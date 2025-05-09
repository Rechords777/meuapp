# Lista de Tarefas do Projeto: Sistema de Rastreamento de Tráfego e Detecção de Cliques Inválidos

Este arquivo rastreia o progresso do desenvolvimento do sistema completo.

## Backend (Flask)

*   [x] **Etapa 1: Configuração Inicial do Projeto Backend**
    *   [x] Criar a estrutura de diretórios do projeto Flask (`create_flask_app traffic_tracker_backend`).
    *   [x] Inicializar o ambiente virtual (`venv`).
    *   [x] Instalar dependências iniciais (Flask, Flask-SQLAlchemy, psycopg2-binary, Flask-Migrate, python-dotenv, requests, Flask-WTF para formulários seguros, Flask-Login para autenticação, Flask-CORS para permitir requisições do frontend, Flask-SocketIO, reportlab, weasyprint).
    *   [x] Configurar o banco de dados (PostgreSQL) e SQLAlchemy no `src/main.py`.
    *   [x] Criar modelos de dados iniciais (ex: `EventLog`, `InvalidClickRule`, `User`) em `src/models/`.
    *   [x] Configurar migrações com Flask-Migrate. (PENDENTE: Servidor PostgreSQL precisa estar em execução para `flask db migrate` e `flask db upgrade`)
    *   [x] Criar arquivo `.env` para variáveis de ambiente (chaves de API, configuração do banco de dados).
*   [x] **Etapa 2: Implementação dos Endpoints da API RESTful**
    *   [x] Criar Blueprint para eventos (`src/routes/events.py`).
    *   [x] Implementar endpoint `POST /event` para registrar cliques/conversões.
    *   [x] Criar Blueprint para métricas (`src/routes/metrics.py`).
    *   [x] Implementar endpoint `GET /metrics` para buscar métricas filtradas.
    *   [x] Criar Blueprint para exportação (`src/routes/export.py`).
    *   [x] Implementar endpoint `GET /export` para exportar dados em CSV e PDF.
    *   [x] Criar Blueprint para logs (`src/routes/logs.py`).
    *   [x] Implementar endpoint `GET /logs` para listar logs e alertas.
*   [x] **Etapa 3: Implementação do WebSocket para Tempo Real**
    *   [x] Integrar Flask-SocketIO ou similar para comunicação WebSocket.
    *   [x] Emitir event*   [x] **Etapa 4: Desenvolvimento do Módulo de Detecção de Cliques Inválidos**
    *   [x] Criar módulo/serviço `src/services/click_validator.py`.
    *   [x] Implementar lógica para detecção por frequência de IP (com ressalva da dependência do DB).
    *   [x] Implementar lógica para detecção por User Agent suspeito (usar lista de referência).
    *   [x] Implementar lógica para detecção por geolocalização incomum (requer integração com `ipapi.co` e dados da campanha).
    *   [x] Integrar o `click_validator` como middleware ou chamá-lo no endpoint `/event`.   *   [ ] Criar serviço `src/services/geolocation.py` para interagir com `ipapi.co`.
    *   [ ] Chamar o serviço de geolocalização ao registrar um evento.
    *   [ ] Implementar fallback para "geolocalização desconhecida".
*   [ ] **Etapa 6: Sistema de Logging Detalhado**
    *   [ ] Configurar logging do Flask para registrar eventos no formato JSON especificado.
    *   [ ] Garantir que todos os campos (IP, User Agent, timestamp, país, canal, dispositivo, validade, razão) sejam logados.
*   [ ] **Etapa 7: Geração e Exportação de Relatórios**
    *   [ ] Implementar a lógica de geração de CSV no endpoint `/export`.
    *   [ ] Implementar a lógica de geração de PDF (usando ReportLab ou WeasyPrint) no endpoint `/export`.
    *   [ ] Garantir que os filtros de `/metrics` sejam aplicados na exportação.
*   [ ] **Etapa 8: Configuração de Alertas e Thresholds**
    *   [ ] Implementar leitura de thresholds do arquivo `.env`.
    *   [ ] (Opcional) Criar endpoint de administração (`src/routes/admin.py`) para gerenciar thresholds (requer autenticação).
*   [x] **Etapa 9: Integração com API do Google Ads**
    *   [x] Criar módulo `src/services/google_ads_manager.py`.
    *   [x] Implementar autenticação OAuth 2.0 com a API do Google Ads (requer configuração de `google-ads.yaml` ou variáveis de ambiente).
    *   [x] Implementar funcionalidade para adicionar IPs à lista de exclusão de campanhas (simulado por enquanto, requer API real para testes).
    *   [x] Chamar o `google_ads_manager` quando um clique inválido de alto risco for detectado (placeholder no `events.py`).
    *   [x] Implementar logging para tentativas de integração e fallback.
    *   [ ] Implementar autenticação para o painel de administração (se houver).
    *   [ ] Aplicar medidas de segurança (validação de entrada, proteção CSRF/XSS, etc.).
*   [ ] **Etapa 11: Testes e Validação**
    *   [ ] Escrever testes unitários para os principais módulos e serviços.
    *   [ ] Realizar testes de integração dos endpoints da API.
    *   [ ] Validar a funcionalidade de detecção de cliques inválidos.
    *   [ ] Testar a integração com Google Ads em ambiente de sandbox (se possível).
*   [ ] **Etapa 12: Documentação da API**
    *   [ ] Gerar documentação da API (ex: usando Flask-Swagger ou similar).

*   [x] **Etapa F1: Configuração Inicial do Projeto Frontend**
    *   [x] Criar a estrutura de diretórios do projeto Next.js (`create_nextjs_app traffic_tracker_frontend`).
    *   [x] Instalar dependências adicionais (ex: `socket.io-client`, `axios`, `recharts`, `date-fns`).
    *   [x] Configurar conexão com o backend Flask (variáveis de ambiente para URL da API).
*   [x] **Etapa F2: Desenvolvimento do Painel em Tempo Real**
    *   [x] Criar layout principal do dashboard (header, sidebar, content area).
    *   [x] Implementar conexão WebSocket com o backend (`/tracking` namespace).
    *   [x] Exibir eventos recebidos em tempo real em uma tabela/lista.
    *   [x] Mostrar contadores/métricas principais atualizados em tempo real.
*   [x] **Etapa F3: Implementação de Filtros Avançados**
    *   [x] Desenvolver componentes de UI para filtros (seletores de data, dropdowns para canal, país, dispositivo, status).
    *   [x] Aplicar filtros às chamadas da API para `/metrics` e `/logs`.
    *   [x] (Opcional) Filtrar dados exibidos em tempo real no frontend.
*   [x] **Etapa F4: Visualização de Métricas e Gráficos**
    *   [x] Integrar com o endpoint `/api/metrics` para buscar dados agregados.
    *   [x] Exibir métricas em cards ou seções dedicadas.
    *   [ ] Implementar gráficos (ex: eventos ao longo do tempo, distribuição por país) usando Recharts.
*   [x] **Etapa F5: Visualização e Filtragem de Logs Detalhados**
    *   [x] Integrar com o endpoint `/api/logs` para buscar logs paginados.
    *   [x] Exibir logs em uma tabela com paginação.
    *   [x] Permitir que os filtros da Etapa F3 se apliquem à visualização de logs.
*   [x] **Etapa F6: Funcionalidade de Exportação de Relatórios (via API)**
    *   [x] Criar interface para o usuário selecionar filtros e formato de exportação (CSV/PDF).
    *   [x] Chamar o endpoint `/api/export` do backend e permitir o download do arquivo gerado.
*   [x] **Etapa F7: Interface para Configuração de Alertas (se aplicável no frontend)**
    *   [x] (Se houver endpoint de admin no backend) Criar interface para visualizar/modificar thresholds de alerta.
*   [ ] **Etapa F8: Autenticação e Gerenciamento de Usuário (se aplicável)**
    *   [ ] (Se o backend implementar autenticação) Criar páginas de login/registro.
    *   [ ] Proteger rotas do dashboard.
*   [ ] **Etapa F9: Testes e Validação do Frontend**
    *   [ ] Testar a responsividade em diferentes dispositivos.
    *   [ ] Validar a funcionalidade de todos os componentes e integrações.
    *   [ ] Realizar testes de usabilidade.

## Deploy

*   [x] **Etapa D1: Preparação para Deploy do Backend**
    *   [x] Garantir que `requirements.txt` esteja atualizado.
    *   [ ] Configurar variáveis de ambiente para produção (simulado/local, DB pendente).
*   [ ] **Etapa D2: Deploy do Backend (Flask)** (FALHOU: Dependências nativas como psycopg2-binary e Pillow não são suportadas no ambiente de deploy serverless. Alternativas: usar pg8000, bibliotecas puras para imagem, ou deploy em VM/container).
*   [ ] **Etapa D3: Preparação para Deploy do Frontend**
*   [ ] **Etapa D4: Deploy do Frontend (Static/Next.js)**
*   [ ] **Etapa D5: Configuração de Domínio e HTTPS**


