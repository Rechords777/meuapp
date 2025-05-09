# Checklist de Testes e Validação

Este checklist visa garantir que todas as funcionalidades principais do Sistema de Rastreamento de Tráfego e Detecção de Cliques Inválidos sejam testadas e validadas antes do deploy final.

## I. Testes do Backend (Flask)

1.  **[ ] Configuração e Inicialização:**
    *   [ ] Verificar se a aplicação Flask inicia sem erros.
    *   [ ] Confirmar a conexão com o banco de dados PostgreSQL.
    *   [ ] Validar se as migrações do banco de dados (Flask-Migrate) foram aplicadas corretamente (PENDENTE: requer servidor PostgreSQL operacional).
2.  **[ ] Endpoints da API RESTful:**
    *   **Eventos (`/api/event`):**
        *   [ ] Testar o registro de novos eventos (cliques/visualizações) com dados válidos.
        *   [ ] Testar o registro com dados inválidos ou ausentes (verificar tratamento de erro).
        *   [ ] Verificar se a geolocalização por IP está funcionando (ipapi.co).
        *   [ ] Confirmar se o `click_validator` é acionado e classifica o evento corretamente.
        *   [ ] Verificar se o evento é emitido via WebSocket para o namespace `/tracking`.
    *   **Métricas (`/api/metrics`):**
        *   [ ] Testar a busca de métricas sem filtros.
        *   [ ] Testar a busca de métricas com diferentes combinações de filtros (data, canal, país, dispositivo, status).
        *   [ ] Validar a precisão dos dados retornados (total de eventos, cliques válidos/inválidos, IPs únicos).
    *   **Logs (`/api/logs`):**
        *   [ ] Testar a busca de logs sem filtros, com paginação.
        *   [ ] Testar a busca de logs com diferentes combinações de filtros.
        *   [ ] Validar a paginação (número correto de itens por página, navegação entre páginas).
    *   **Exportação (`/api/export`):**
        *   [ ] Testar a exportação de dados em formato CSV com e sem filtros.
        *   [ ] Testar a exportação de dados em formato PDF com e sem filtros.
        *   [ ] Verificar a integridade e o formato dos arquivos exportados.
3.  **[ ] Lógica de Detecção de Cliques Inválidos (`src/services/click_validator.py`):**
    *   [ ] Testar a detecção por frequência de IP (requer dados no DB).
    *   [ ] Testar a detecção por User Agent suspeito (usar UAs da lista e UAs válidos).
    *   [ ] Testar a detecção por geolocalização inconsistente (se dados da campanha forem fornecidos).
    *   [ ] Verificar se os motivos da invalidação são registrados corretamente.
4.  **[ ] Integração com Google Ads (`src/services/google_ads_manager.py`):**
    *   [ ] (SIMULADO/PENDENTE DE CREDENCIAIS REAIS) Testar a adição de IPs à lista de exclusão de campanhas.
    *   [ ] Verificar o tratamento de erros na comunicação com a API do Google Ads.
5.  **[ ] WebSockets (Flask-SocketIO):**
    *   [ ] Confirmar que o servidor WebSocket está operacional no namespace `/tracking`.
    *   [ ] Verificar se novos eventos são emitidos corretamente para os clientes conectados.

## II. Testes do Frontend (Next.js)

1.  **[ ] Configuração e Conexão:**
    *   [ ] Verificar se a aplicação Next.js inicia sem erros.
    *   [ ] Confirmar se as variáveis de ambiente para API_URL e WS_URL estão corretas.
2.  **[ ] Painel em Tempo Real (`/dashboard`):
    *   **Conexão WebSocket:**
        *   [ ] Verificar se o frontend conecta ao WebSocket do backend.
        *   [ ] Observar o status da conexão (Conectado/Desconectado).
    *   **Exibição de Métricas:**
        *   [ ] Verificar se os cards de métricas (Total de Eventos, Cliques Válidos/Inválidos, IPs Únicos) são carregados inicialmente.
        *   [ ] Confirmar se as métricas são atualizadas em tempo real com a chegada de novos eventos via WebSocket.
    *   **Exibição de Eventos Recentes:**
        *   [ ] Verificar se a tabela de eventos recentes é carregada inicialmente (últimos logs).
        *   [ ] Confirmar se novos eventos são adicionados à tabela em tempo real.
        *   [ ] Verificar a formatação dos dados na tabela (timestamp, IP, país, URL, status, razão).
3.  **[ ] Filtros Avançados:**
    *   [ ] Testar a aplicação de cada filtro individualmente (Data Início/Fim, Canal, País, Tipo de Dispositivo, Status do Clique).
    *   [ ] Testar combinações de múltiplos filtros.
    *   [ ] Verificar se os dados de Métricas e a tabela de Logs de Eventos são atualizados corretamente após aplicar os filtros.
    *   [ ] Testar o botão "Limpar Filtros" para redefinir a visualização.
4.  **[ ] Visualização de Logs Detalhados (com Filtros e Paginação):**
    *   [ ] Confirmar que a tabela de logs reflete os filtros aplicados.
    *   [ ] Testar a funcionalidade de paginação (botões Anterior/Próxima, contagem de páginas/logs).
5.  **[ ] Exportação de Relatórios:**
    *   [ ] Testar a exportação de relatórios (CSV/PDF) a partir da interface.
    *   [ ] Verificar se os filtros aplicados no dashboard são considerados na exportação.
    *   [ ] Confirmar o download e a integridade dos arquivos gerados.
6.  **[ ] Interface de Alertas (se implementada e conectada ao backend):**
    *   [ ] Testar a visualização e modificação de thresholds de alerta.
    *   [ ] Verificar se os alertas são gerados e notificados conforme as configurações.
7.  **[ ] Responsividade e Usabilidade:**
    *   [ ] Testar a interface em diferentes tamanhos de tela (desktop, tablet, mobile).
    *   [ ] Avaliar a clareza das informações e a facilidade de navegação.
    *   [ ] Verificar se todos os elementos interativos (botões, inputs, selects) funcionam como esperado.

## III. Testes de Integração (End-to-End)

1.  **[ ] Fluxo Completo de Evento:**
    *   [ ] Simular um novo clique/evento (ex: usando uma ferramenta como Postman para o endpoint `/api/event` ou através de um script de teste no frontend, se houver).
    *   [ ] Observar o registro no backend (logs do Flask, banco de dados se acessível).
    *   [ ] Verificar a atualização em tempo real no dashboard do frontend (métricas e tabela de eventos).
    *   [ ] Se o evento for inválido e a integração com Google Ads estiver ativa (mesmo simulada), verificar se a lógica de exclusão de IP é acionada.
2.  **[ ] Consistência de Dados:**
    *   [ ] Verificar se os dados exibidos no frontend (métricas, logs) correspondem aos dados no backend após aplicar filtros e realizar ações.

## IV. Testes Não Funcionais

1.  **[ ] Segurança (Básica):**
    *   [ ] Revisar se há proteção contra vulnerabilidades comuns (XSS, CSRF - o template Next.js e Flask oferecem alguma base).
    *   [ ] Verificar se dados sensíveis (como chaves de API) não estão expostos no código do frontend.
2.  **[ ] Performance (Observacional):**
    *   [ ] Observar o tempo de carregamento das páginas do frontend.
    *   [ ] Observar o tempo de resposta da API do backend para requisições com e sem filtros.

## V. Documentação

1.  **[ ] `README.md` do Backend:**
    *   [ ] Verificar se contém instruções claras de configuração, execução e endpoints da API.
2.  **[ ] `README.md` do Frontend:**
    *   [ ] Verificar se contém instruções claras de configuração, execução e como interagir com o dashboard.
3.  **[ ] `todo.md`:**
    *   [ ] Confirmar que todas as tarefas planejadas foram abordadas e seu status está correto.
4.  **[ ] `backend_requirements.md` e outros artefatos:**
    *   [ ] Revisar se os documentos de requisitos e planejamento estão consistentes com o produto final.

**Observação:** Alguns testes, especialmente os que dependem de um servidor PostgreSQL operacional e credenciais reais do Google Ads, podem precisar ser adaptados ou realizados em um ambiente de homologação/produção.
