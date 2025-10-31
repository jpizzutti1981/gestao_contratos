# Gestão de Contratos – Preparação para Git

Este projeto foi testado diretamente em uma VM. Fizemos ajustes para torná-lo seguro para versionamento: variáveis sensíveis agora vêm do `.env`, sinais de criação de perfil foram centralizados em `usuarios`, e adicionamos `.gitignore` e `.env.example` na raiz.

## Requisitos
- Python 3.10+
- Pip / venv
- Docker e Docker Compose (opcional)

## Configuração do ambiente
1. Crie um ambiente virtual e instale dependências:
   - `python -m venv venv`
   - `venv\Scripts\activate` (Windows)
   - `pip install -r requirements.txt`
2. Crie o arquivo `.env` na raiz, baseado em `.env.example`:
   - `SECRET_KEY` – gere uma chave segura em produção
   - `DEBUG` – `True` para desenvolvimento, `False` em produção
   - `ALLOWED_HOSTS` – domínios/hosts permitidos (separados por vírgula)
   - `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_FROM` – credenciais SMTP

## Execução local
- Aplique migrações e rode o servidor:
  - `python manage.py migrate`
  - `python manage.py createsuperuser`
  - `python manage.py runserver`
- Coleta de estáticos (se necessário):
  - `python manage.py collectstatic`

## Sinais e perfis
- Os sinais de criação automática de `Perfil` para o modelo customizado `Usuario` estão em `usuarios/signals.py`.
- O app `usuarios` possui `UsuariosConfig` em `usuarios/apps.py`, registrado em `INSTALLED_APPS` para garantir que os sinais sejam carregados.
- Removemos sinais duplicados que referenciavam `User` (nativo) para evitar inconsistências.

## Scripts úteis
- Corrigir usuários sem perfil:
  - `python corrigir_usuarios_sem_perfil.py`
  - O script usa `usuarios.models.Perfil` e o campo `usuario` corretamente.

## Docker
- Há `Dockerfile` e `docker-compose.yml` no projeto.
- Exemplo de uso:
  - `docker compose up -d --build`
  - Ajuste o `.env` conforme o ambiente do container (não comitar o `.env`).

## Boas práticas de versionamento
- `.gitignore` na raiz já ignora `venv/`, `.env`, `db.sqlite3`, `uploads/`, `__pycache__/`, e arquivos temporários.
- Nunca comitar o `.env` nem credenciais reais.
- Antes de publicar:
  - Confira `DEBUG=False` e `ALLOWED_HOSTS` corretos em produção.
  - Defina `SECRET_KEY` seguro via `.env`.

## Inicializar repositório Git
- `git init`
- `git add .`
- `git commit -m "chore: inicialização do repositório"`
- Crie o repositório remoto (GitHub/GitLab/Bitbucket) e faça `git remote add origin ...` seguido de `git push -u origin main`.

## Observações
- Banco padrão é SQLite (dev). Para produção, recomenda-se Postgres com variáveis de conexão via `.env`.
- Se usar Nginx/Apache para estáticos, configure `STATIC_ROOT` e execute `collectstatic` no build/deploy.