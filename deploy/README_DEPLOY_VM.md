# Deploy na VM (Ubuntu)

Guia prático para publicar o projeto `gestao_contratos` em uma VM Linux (ex.: Ubuntu 22.04), usando Gunicorn + Nginx.

## Pré-requisitos
- VM com acesso SSH e domínio/IP público.
- Python 3.10+ e `venv` instalados.
- Nginx instalado (`sudo apt-get install -y nginx`).
- Usuário com permissões para `sudo`.

## Caminhos e variáveis usadas
- Código: `/srv/gestao_contratos`
- Venv: `/srv/gestao_contratos/venv`
- Logs: `/var/log/gestao_contratos`
- Arquivo `.env`: `/etc/gestao_contratos/.env`
- Porta Gunicorn: `127.0.0.1:8001` (privada, atrás do Nginx)

Adapte os caminhos conforme sua realidade.

## Passo a passo

1. Atualize a VM e instale dependências principais:
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   sudo apt-get install -y python3-venv python3-pip git nginx
   ```

2. Crie diretórios e clone o projeto:
   ```bash
   sudo mkdir -p /srv/gestao_contratos /var/log/gestao_contratos /etc/gestao_contratos
   sudo chown -R $USER:$USER /srv/gestao_contratos /var/log/gestao_contratos /etc/gestao_contratos
   cd /srv/gestao_contratos
   git clone https://github.com/jpizzutti1981/gestao_contratos.git .
   ```

3. Crie a virtualenv e instale dependências:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install gunicorn
   ```

4. Configure variáveis de ambiente:
   ```bash
   sudo nano /etc/gestao_contratos/.env
   ```
   Exemplos mínimos (ajuste conforme seu `settings.py`):
   ```env
   DEBUG=False
   SECRET_KEY=troque_por_uma_chave_segura
   ALLOWED_HOSTS=seu.dominio.com,IP_DA_VM
   CSRF_TRUSTED_ORIGINS=https://seu.dominio.com
   DATABASE_URL=postgres://usuario:senha@localhost:5432/gestao_contratos
   STATIC_ROOT=/srv/gestao_contratos/staticfiles
   MEDIA_ROOT=/srv/gestao_contratos/media
   ```

5. Rode migrações e colete estáticos:
   ```bash
   chmod +x deploy/scripts/migrate_collectstatic.sh
   APP_DIR=/srv/gestao_contratos VENV_DIR=/srv/gestao_contratos/venv ./deploy/scripts/migrate_collectstatic.sh
   ```

6. Configure o serviço do Gunicorn (systemd):
   ```bash
   sudo cp deploy/systemd/gestao_contratos.service /etc/systemd/system/gestao_contratos.service
   sudo systemctl daemon-reload
   sudo systemctl enable gestao_contratos
   sudo systemctl start gestao_contratos
   sudo systemctl status gestao_contratos --no-pager
   ```

7. Configure o Nginx:
   ```bash
   sudo cp deploy/nginx/gestao_contratos.conf /etc/nginx/sites-available/gestao_contratos.conf
   sudo ln -sf /etc/nginx/sites-available/gestao_contratos.conf /etc/nginx/sites-enabled/gestao_contratos.conf
   sudo nginx -t
   sudo systemctl reload nginx
   ```
   - Edite `server_name` no arquivo para seu domínio/IP.
   - Ajuste `alias` de `static` e `media` se você usar caminhos diferentes.

8. Certificado TLS (opcional, recomendado):
   ```bash
   sudo apt-get install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d seu.dominio.com
   ```

9. Logs e verificação:
   ```bash
   sudo journalctl -u gestao_contratos -f
   sudo tail -f /var/log/gestao_contratos/gunicorn.error.log
   sudo tail -f /var/log/nginx/error.log
   ```

## Dicas
- Sempre verifique `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`.
- Desative `DEBUG` em produção.
- Configure banco de dados (PostgreSQL, MySQL) conforme sua VM.
- Se alterar paths, atualize o service do systemd e o Nginx.