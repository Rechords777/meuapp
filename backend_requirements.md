# Requisitos do Backend para o Sistema de Rastreamento de Tráfego e Detecção de Cliques Inválidos

Este documento detalha os requisitos funcionais e técnicos para o backend do sistema, com base nas especificações fornecidas.

## 1. API RESTful
O backend deverá expor uma API RESTful com os seguintes endpoints:

*   **`POST /event`**: Para registrar um novo evento de clique ou conversão. O corpo da requisição deverá conter informações relevantes como IP, User Agent, URL de origem, etc.
*   **`GET /metrics`**: Para buscar métricas agregadas de tráfego e cliques. Deverá suportar filtros por período, canal, dispositivo, país, e status (válido/inválido).
*   **`GET /export`**: Para exportar dados de eventos e métricas. Deverá suportar os formatos CSV e PDF, especificados através de um parâmetro de query (ex: `?format=csv` ou `?format=pdf`). Os dados exportados devem respeitar os filtros aplicados em `/metrics`.
*   **`GET /logs`**: Para listar logs detalhados de eventos, incluindo alertas de cliques inválidos e tentativas de integração (ex: Google Ads).

## 2. Comunicação em Tempo Real com WebSocket
O sistema deverá implementar um servidor WebSocket para enviar atualizações em tempo real para o painel frontend a cada novo clique ou conversão registrada. Isso permitirá a visualização dinâmica dos dados.

## 3. Módulo de Detecção de Cliques Inválidos
Um middleware ou módulo dedicado será responsável por analisar cada evento recebido e classificá-lo como válido ou inválido. Os critérios de detecção incluem:

*   **Frequência de Cliques por IP**: Identificar um número excessivo de cliques de um mesmo endereço IP em um curto intervalo de tempo (ex: mais de 5 cliques em 10 segundos). Os thresholds serão configuráveis.
*   **User Agent Suspeito**: Detectar User Agents conhecidos por pertencerem a bots, crawlers, ou ferramentas de CLI, ou User Agents vazios/genéricos.
*   **Geolocalização Incomum**: Verificar se a geolocalização do IP do clique é inconsistente com a segmentação geográfica esperada para uma campanha específica (quando aplicável).

## 4. Integração com API de Geolocalização de IP
O sistema se integrará com a API `ipapi.co` para obter informações de geolocalização (país, cidade, etc.) com base no endereço IP do evento. Em caso de falha na API, a geolocalização será registrada como "desconhecida".

## 5. Sistema de Logging Detalhado
Todos os eventos processados (cliques, conversões) deverão ser registrados em logs. Cada registro de log deverá conter, no mínimo:

*   Endereço IP
*   User Agent
*   Timestamp do evento
*   País (obtido via geolocalização)
*   Canal de origem (ex: Google Ads, Orgânico)
*   Tipo de dispositivo (ex: mobile, desktop)
*   Status de validade (válido/inválido)
*   Razão da invalidade (se aplicável, ex: "alta frequência de IP", "User Agent suspeito")

Os logs seguirão um formato JSON padronizado, conforme especificado:
```json
{
  "ip": "192.168.0.1",
  "userAgent": "Mozilla/5.0",
  "timestamp": "2025-04-30T15:00:00Z",
  "country": "BR",
  "channel": "Google Ads",
  "device": "mobile",
  "valid": false,
  "reason": "userAgent=crawler"
}
```

## 6. Geração e Exportação de Relatórios
O sistema permitirá a exportação de relatórios nos formatos CSV e PDF. Os relatórios conterão dados de eventos e métricas, podendo ser filtrados conforme os critérios disponíveis na API (`/metrics`). Serão utilizadas bibliotecas apropriadas para a geração desses formatos (ex: `csv` para CSV, `ReportLab` ou `WeasyPrint` para PDF).

## 7. Configuração de Alertas e Thresholds
Os thresholds para a detecção de cliques inválidos (ex: número de cliques por IP em um intervalo de tempo) serão configuráveis. Essa configuração poderá ser feita através de variáveis de ambiente (`.env`) ou, opcionalmente, por meio de um endpoint de administração protegido.

## 8. Integração com a API do Google Ads
O backend deverá se integrar com a API do Google Ads para:

*   **Proteção de Campanhas**: Adicionar automaticamente endereços IP identificados como fontes de cliques inválidos à lista de exclusão de IP das campanhas ativas no Google Ads. Isso ajudará a proteger o orçamento publicitário em tempo real.
*   **Otimização de Orçamento**: Fornecer dados e insights que possam ser utilizados para otimizar o investimento em publicidade, com base nos padrões de tráfego válido e inválido detectados.

A integração utilizará OAuth 2.0 para autenticação. Em caso de falha na integração (ex: erro ao adicionar IP à lista de exclusão), o evento será logado e uma notificação poderá ser gerada.

## 9. Banco de Dados
Será utilizado um banco de dados relacional (PostgreSQL é o preferido para aplicações Flask com SQLAlchemy) para armazenar os eventos, logs, configurações e outros dados persistentes da aplicação.

## 10. Tecnologia e Estrutura do Backend
O backend será desenvolvido utilizando Python com o framework Flask. A estrutura do projeto seguirá as melhores práticas para aplicações Flask, incluindo:

*   Uso de Blueprints para organizar rotas.
*   SQLAlchemy como ORM para interações com o banco de dados.
*   Gerenciamento de dependências com `pip` e `requirements.txt`.
*   Ambiente virtual (`venv`) para isolamento do projeto.
*   Estrutura de diretórios organizada (ex: `src/models`, `src/routes`, `src/services`, `src/utils`, `main.py` como ponto de entrada).

## 11. Fallbacks e Tratamento de Erros
O sistema deverá implementar mecanismos de fallback para garantir resiliência:

*   Se a API de geolocalização de IP falhar, registrar a geolocalização como "desconhecida".
*   Se a exportação para PDF falhar, oferecer a exportação em CSV como alternativa ou registrar o erro.
*   Se a integração com o Google Ads falhar, registrar a tentativa e o erro, e opcionalmente notificar um administrador.

## 12. Considerações de Segurança
*   Validação de entrada em todos os endpoints da API.
*   Proteção contra ataques comuns (XSS, CSRF, SQL Injection).
*   Gerenciamento seguro de chaves de API e credenciais (ex: via variáveis de ambiente).
*   Autenticação e autorização para endpoints sensíveis (ex: configuração, integração com Google Ads).

