## Plano de Desenvolvimento - Sistema de Rastreamento de Tráfego e Detecção de Cliques Inválidos

**Objetivo:** Desenvolver um sistema web completo para rastrear tráfego, detectar cliques inválidos e fornecer relatórios e alertas em tempo real.

**Fases do Projeto:**

**Fase 1: Backend (Flask)**

1.  **[FEITO]** Configuração Inicial:
    *   [x] Criar a estrutura de diretórios do projeto.
    *   [x] Inicializar um ambiente virtual Python.
    *   [x] Instalar dependências essenciais (Flask, Flask-SQLAlchemy, Flask-Migrate, etc.).
    *   [x] Configurar o banco de dados (PostgreSQL) e o SQLAlchemy.
    *   [x] Implementar a lógica de migração do banco de dados com Flask-Migrate.

2.  **[FEITO]** Modelagem de Dados:
    *   [x] Definir o modelo `EventLog` para armazenar dados de eventos (IP, User-Agent, Timestamp, URL Acessada, etc.).
    *   [x] Definir o modelo `InvalidClickRule` para armazenar regras de detecção de cliques inválidos.
    *   [x] Definir outros modelos conforme necessário (ex: Usuários, Campanhas, etc.).

3.  **[FEITO]** Endpoints da API RESTful:
    *   [x] `POST /event`: Receber dados de eventos (cliques, visualizações de página, etc.).
    *   [x] `GET /metrics`: Retornar métricas agregadas (ex: contagem de eventos, cliques válidos/inválidos).
    *   [x] `GET /logs`: Listar eventos com opções de filtragem e paginação.
    *   [x] `POST /rules`: Adicionar/atualizar regras de detecção de cliques inválidos.
    *   [x] `GET /rules`: Listar regras de detecção de cliques inválidos.
    *   [x] `DELETE /rules/<rule_id>`: Excluir uma regra de detecção.

4.  **[FEITO]** Lógica de Detecção de Cliques Inválidos:
    *   [x] Implementar a lógica para analisar os dados dos eventos recebidos.
    *   [x] Aplicar as regras de detecção de cliques inválidos (ex: frequência de IP, padrões de User-Agent, geolocalização suspeita).
    *   [x] Marcar eventos como válidos ou inválidos e armazenar o motivo da invalidação.

5.  **[FEITO]** Integração com Google Ads (Opcional, mas recomendado):
    *   [x] Pesquisar e implementar a API do Google Ads para exclusão de IPs.
    *   [x] Desenvolver funcionalidade para adicionar IPs detectados como inválidos à lista de exclusão de campanhas no Google Ads.

6.  **[FEITO]** Testes Unitários e de Integração:
    *   [x] Escrever testes para garantir a funcionalidade e a confiabilidade do backend.

**Fase 2: Frontend (Next.js e Tailwind CSS)**

1.  **[FEITO]** Configuração Inicial do Projeto:
    *   [x] Criar um novo projeto Next.js.
    *   [x] Configurar Tailwind CSS para estilização.
    *   [x] Definir a estrutura de pastas e componentes.

2.  **[FEITO]** Interface do Usuário (UI):
    *   [x] **Página de Login:** (Se aplicável) Interface para autenticação de usuários.
    *   [x] **Dashboard Principal:** Exibir métricas chave, gráficos e uma visão geral dos eventos recentes.
    *   [x] **Visualização de Eventos:** Tabela ou lista para exibir eventos detalhados, com opções de filtragem e paginação.
    *   [x] **Gerenciamento de Regras:** Interface para visualizar, criar, editar e excluir regras de detecção de cliques inválidos.
    *   [x] **Configurações:** Opções para configurar o sistema (ex: limites de alerta, integrações).

3.  **[FEITO]** Integração com o Backend:
    *   [x] Utilizar `axios` ou `fetch` para fazer requisições à API Flask.
    *   [x] Implementar lógica para exibir dados recebidos do backend.
    *   [x] Criar formulários para interagir com os endpoints da API (ex: adicionar regras, modificar configurações).

4.  **[FEITO]** Visualização de Dados:
    *   [x] Utilizar bibliotecas de gráficos (ex: Recharts, Chart.js) para exibir dados de forma visual.
    *   [x] Implementar filtros e opções de ordenação para tabelas de dados.

5.  **[FEITO]** Notificações em Tempo Real (Opcional):
    *   [x] Utilizar WebSockets (ex: Socket.IO) para exibir novos eventos em tempo real no dashboard.

6.  **[FEITO]** Testes e Validação:
    *   [x] Testar a interface do usuário em diferentes navegadores e dispositivos.
    *   [x] Garantir a usabilidade e a acessibilidade da interface.

**Fase 3: Integração e Implantação**

1.  **[FEITO]** Testes End-to-End:
    *   [x] Testar o fluxo completo da aplicação, desde a coleta de dados até a exibição no frontend.

2.  **[FEITO]** Otimização e Performance:
    *   [x] Otimizar o desempenho do backend e do frontend.
    *   [x] Garantir que a aplicação seja escalável para lidar com um grande volume de dados.

3.  **[FEITO]** Documentação:
    *   [x] Documentar a API e o código-fonte.
    *   [x] Criar um manual do usuário para o sistema.

4.  **[FEITO]** Implantação:
    *   [x] Escolher uma plataforma de hospedagem (ex: AWS, Google Cloud, Heroku, Vercel).
    *   [x] Configurar o ambiente de produção.
    *   [x] Implantar a aplicação.

**Tecnologias Sugeridas:**

*   **Backend:** Python (Flask ou FastAPI)
*   **Frontend:** Next.js (React)
*   **Banco de Dados:** PostgreSQL
*   **Comunicação em Tempo Real (Opcional):** Socket.IO
*   **Outras Ferramentas:** Docker, Git, etc.

**Considerações Adicionais:**

*   **Segurança:** Implementar medidas de segurança adequadas para proteger os dados e a aplicação.
*   **Escalabilidade:** Projetar a arquitetura para suportar um aumento no volume de tráfego e dados.
*   **Manutenibilidade:** Escrever código limpo, bem documentado e testável para facilitar a manutenção futura.
*   **Usabilidade:** Criar uma interface intuitiva e fácil de usar para os usuários finais.

Este plano de desenvolvimento é um ponto de partida e pode ser ajustado conforme necessário durante o projeto. A comunicação regular e a colaboração entre as equipes de backend e frontend são cruciais para o sucesso do projeto.
