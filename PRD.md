# PRD — Sistema de Gestão de Contratos e Documentos

## 1. Visão Geral
- Objetivo: centralizar o cadastro, envio, aprovação e acompanhamento de documentos e contratos por shopping, com controle de obrigações, vencimentos e indicadores gerenciais.
- Contexto: utilizado por três perfis principais (Corporativo, Gestor, Usuário), com um painel administrativo para gestão de shoppings e usuários.
- Resultado esperado: redução de riscos de vencimentos, maior transparência nos status, e padronização do fluxo documental.

## 2. Escopo
- Em escopo:
  - Autenticação e redirecionamento por perfil.
  - Painel gerencial de documentos obrigatórios com KPIs, filtros e ações (marcar OK, vincular, importar Excel, excluir).
  - Painel por shopping com lista de documentos, status e ações.
  - Fluxo de envio (upload) de documentos com múltiplos anexos.
  - Aprovação/Reprovação pelo Gestor, com histórico e notificações.
  - Agenda de vencimentos com API para calendário.
  - Painel administrativo (shoppings, usuários, grupos e perfis).
- Fora de escopo (nesta versão):
  - Integração com armazenamento externo (S3, etc.).
  - Workflow multi-etapa de aprovação com regras customizadas.
  - Assinatura eletrônica e verificação de integridade dos arquivos.

## 3. Personas e Perfis de Acesso
- Corporativo:
  - Vê todos os shoppings e obrigações.
  - Pode importar obrigações via Excel.
  - Pode marcar OK, vincular/desvincular documentos e excluir obrigações.
- Gestor:
  - Atua sobre seu shopping (via `Perfil.shopping`).
  - Aprova/Reprova documentos, insere novos documentos, consulta agenda.
- Usuário:
  - Usuário comum associado diretamente a um `Shopping`.
  - Pode enviar documentos do seu shopping e consultar seus registros.
- Superuser/Admin:
  - Acesso total, incluindo painel administrativo.

## 4. Jornadas Principais
- Acesso e Redirecionamento
  - Login em `/accounts/login/`.
  - Redirecionamento pós-login conforme grupo:
    - Corporativo → `painel_geral`.
    - Gestor → `pendencias_gestor` (se perfil configurado; senão, erro e logout).
    - Usuário → `detalhes_shopping` (se associado a um shopping; senão, erro e logout).
- Corporativo (Painel Gerencial de Obrigações)
  - Visualiza KPIs: Total, Pendentes, Concluídos.
  - Filtra por Área, Categoria, Shopping e Status.
  - Ações em linha: marcar OK, vincular documento avulso, desvincular, excluir.
  - Importa obrigações via Excel (com mapeamento flexível de colunas).
- Gestor (Pendências + Shopping)
  - Vê pendências de aprovação.
  - Detalha documentos do shopping com status de prazo (Em dia, A vencer, Vencido) e aprovação (Pendente/Aprovado/Reprovado).
  - Envia documentos e gerencia anexos.
  - Aprova/Reprova documentos com registro do motivo.
- Usuário
  - Envia documentos do shopping e acompanha seus registros.
- Agenda
  - Acompanha vencimentos por cor (verde, amarelo, vermelho) e navega ao detalhe.
- Admin
  - Gerencia shoppings, usuários, grupos e perfis.

## 5. Requisitos Funcionais
### 5.1 Autenticação e Navegação
- Login em `registration/login.html` com feedback de sucesso/erro.
- Rotas centrais:
  - `path('', painel_redirect)`
  - `path('painel/geral/', painel_documentos)`
  - `path('painel/gerencial/', PainelDocumentosView)`
  - `path('painel/shopping/<id>/', detalhes_shopping)`
  - `path('painel/pendencias/', pendencias_gestor)`
  - `path('accounts/login/', CustomLoginView)`
  - `path('accounts/logout/', CustomLogoutView)`

### 5.2 Documentos (RegistroDocumento)
- Dados:
  - `shopping`, `titulo`, `tipo` (documento|contrato), `descricao`, `data_emissao`, `data_vencimento`, `enviado_por`, `data_envio`, `status_aprovacao` (default pendente), `aprovado_por`, `data_aprovacao`, `motivo_reprovacao`.
- Anexos múltiplos via `AnexoDocumento` (campo `arquivo`, `data_upload`).
- Fluxos:
  - Criar (upload) com múltiplos anexos.
  - Editar (adicionar/excluir anexos) e salvar.
  - Excluir com confirmação.
  - Detalhar com cálculo de URLs de retorno seguro.
  - Aprovar/Reprovar com mensagens e e-mail ao responsável quando aplicável.
- Visualização por shopping com badges de prazo baseadas em `data_vencimento`.

### 5.3 Documentos Obrigatórios (DocumentoObrigatorio)
- Dados:
  - `area`, `categoria`, `nome`, `shopping`, `ativo`, `marcado_ok`, `marcado_por`, `marcado_em`, `documento_vinculado` (para apontar um `RegistroDocumento`).
- Funcionalidades:
  - Criar rápido (form inline no painel gerencial).
  - Importar via Excel (`documento/obrigatorio/importar/`).
  - Marcar OK (gestor/corporativo) com time-stamp e usuário.
  - Vincular/Desvincular um documento avulso para cumprir a obrigação.
  - Buscar avulsos via JSON (`buscar_documentos_avulsos_json`).
- Status exibido:
  - `Enviado` quando há documento vinculado com anexos/registro válido.
  - `Pendente` caso contrário.

### 5.4 Agenda de Vencimentos
- Página: `path('agenda/', agenda_documentos)`.
- API: `path('api/vencimentos/', api_vencimentos_json)` retorna eventos com:
  - `title`, `start` (ISO), `color` (prazos), `url` (link ao detalhe).
- Cores:
  - Vermelho: vencido.
  - Amarelo: vence em até 60 dias.
  - Verde: acima de 60 dias.

### 5.5 Notificações
- E-mail ao Gestor quando novo documento é enviado.
- E-mail de alerta de vencimentos (management command `verificar_vencimentos`).
- Templates de e-mail prontos para alerta e novo documento.

### 5.6 Painel Administrativo
- Rotas em `/admin-panel/` para:
  - Shoppings: listar, criar, editar, excluir.
  - Usuários: listar, criar, editar, excluir (com grupo e shopping).
  - Grupos e Perfis: CRUD básico.

## 6. Regras de Negócio
- Permissões por grupo:
  - Corporativo: acesso geral; pode importar obrigações e operar em qualquer shopping.
  - Gestor: acesso restrito ao `Perfil.shopping`.
  - Usuário: acesso restrito ao `Usuario.shopping`.
- Aprovação de documentos:
  - `status_aprovacao` transita entre `pendente`, `aprovado`, `reprovado`.
  - Registro de `aprovado_por`, `data_aprovacao` e `motivo_reprovacao` quando aplicável.
- Prazo de vencimento:
  - Badges de prazo calculadas por `data_vencimento` (em dia, a vencer, vencido).
- Obrigações:
  - Painel gerencial filtra por `area`, `categoria`, `shopping`, `status`.
  - `marcado_ok` e `documento_vinculado` afetam o status exibido.

## 7. Requisitos Não Funcionais
- Segurança:
  - CSRF em formulários.
  - Autenticação Django e controle por grupos.
  - Validação de `next`/`referer` para redirecionamentos seguros.
- Performance:
  - Paginação em listagens.
  - Debounce em buscas (vinculação no painel gerencial).
- Disponibilidade e Dados:
  - Banco padrão SQLite (ambiente dev); suporte a migração para Postgres.
  - Uploads armazenados em `MEDIA_ROOT`.
- UX:
  - KPIs visuais e overlays de carregamento em operações assíncronas.
  - Tooltips e transições suaves onde aplicável.
- Observabilidade:
  - Mensagens de feedback (sucesso/erro) nos fluxos principais.

## 8. Integrações e Dependências
- Principais libs (`requirements.txt`):
  - `Django==5.2`, `django-widget-tweaks==1.5.0`.
  - `openpyxl` para leitura Excel.
  - `python-decouple`/`python-dotenv` para configuração.
- E-mail SMTP configurável via settings.

## 9. Dados e Modelos
- `Shopping`: `nome`, `sigla`, `cnpj`, `email_alertas`.
- `RegistroDocumento`: campos listados em 5.2.
- `AnexoDocumento`: `documento`, `arquivo`, `data_upload`.
- `DocumentoObrigatorio`: campos listados em 5.3.
- `Usuario` + `Perfil`: associação a `Shopping` por grupo/perfil.

## 10. Métricas de Sucesso
- % de obrigações “Em dia” por shopping.
- Tempo médio de aprovação.
- Redução de documentos vencidos mês a mês.
- Taxa de cobertura de obrigações (com documento vinculado ou marcado OK).

## 11. Roadmap (Próximas Iterações)
- Atualização de KPIs em tempo real (sem full reload).
- Automação de status de obrigação com base em regras (ex.: último anexo válido).
- Exportação CSV/Excel de relatórios.
- Integração de armazenamento externo (S3) e CDN.
- Auditoria detalhada (log de mudanças por usuário).

## 12. Navegação — Rotas Principais
- Painéis e listas:
  - `/painel/geral/` — Painel de documentos gerais.
  - `/painel/gerencial/` — Painel gerencial de obrigações.
  - `/painel/shopping/<id>/` — Detalhes por shopping.
  - `/painel/pendencias/` — Pendências do gestor.
- Documentos:
  - `/documento/novo/` e `/documento/novo/<shopping_id>/` — Upload.
  - `/documento/editar/<tipo>/<doc_id>/` — Edição.
  - `/documento/detalhar/<tipo>/<doc_id>/` — Detalhe.
  - `/documento/reprovar/<doc_id>/`, `/documento/aprovar/<doc_id>/` — Workflow de aprovação.
  - Anexos: `/documento/anexo/excluir/<anexo_id>/`.
- Obrigações:
  - `/documento/obrigatorio/novo/` — Criar obrigação.
  - `/documento/obrigatorio/importar/` — Importar Excel.
  - `/documento/obrigatorio/marcar/<id>/` — Marcar OK.
  - `/documento/obrigatorio/vincular/<id>/` e `/documento/obrigatorio/desvincular/<id>/`.
- Agenda/API:
  - `/agenda/` — Agenda de vencimentos.
  - `/api/vencimentos/` — Eventos JSON para calendário.
- Autenticação:
  - `/accounts/login/`, `/accounts/logout/`.

## 13. Glossário
- Documento avulso: um `RegistroDocumento` que pode ser vinculado a uma obrigação.
- Obrigação: `DocumentoObrigatorio` que descreve um requisito a cumprir.
- Vincular: associar um documento avulso a uma obrigação.
- Marcar OK: sinalizar manualmente o cumprimento da obrigação.

---
Este PRD reflete o estado atual do projeto e serve como base para planejamento e evolução. Ajustes podem ser feitos conforme novas necessidades de negócio surgirem.