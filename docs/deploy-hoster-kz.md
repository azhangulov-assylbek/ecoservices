# Развёртывание на hoster.kz

Нужен **VPS**, а не виртуальный хостинг: проекту нужны PostgreSQL, Docker и позже Redis/Celery.
Рекомендуемая конфигурация для старта: Ubuntu 24.04, 2 vCPU, 4 ГБ RAM, 40+ ГБ диска.

## 1. DNS
В панели hoster.kz для домена ecoservices.kz создайте A-записи на IP вашего VPS:
- `ecoservices.kz` → IP
- `www.ecoservices.kz` → IP

Обновление DNS может занять до нескольких часов.

## 2. Подготовка сервера (по SSH)
```bash
ssh root@IP_СЕРВЕРА
apt update && apt upgrade -y
curl -fsSL https://get.docker.com | sh
ufw allow OpenSSH && ufw allow 80 && ufw allow 443 && ufw --force enable
```

## 3. Код и настройки
```bash
git clone https://github.com/azhangulov-assylbek/ecoservices.git /opt/ecoservices
cd /opt/ecoservices
cp .env.example .env
nano .env        # заполнить секретный ключ и пароли
```
Секретный ключ можно сгенерировать так:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

## 4. Запуск
```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```
Caddy автоматически получит HTTPS-сертификат, когда DNS начнёт указывать на сервер.
Сайт: https://ecoservices.kz, админка: https://ecoservices.kz/admin/

## 5. Обновление
```bash
cd /opt/ecoservices && git pull
docker compose -f docker-compose.prod.yml up -d --build
```

## 6. Резервная копия базы (ежедневно, cron)
```bash
mkdir -p /opt/backups
crontab -e
# добавить строку:
0 3 * * * cd /opt/ecoservices && docker compose -f docker-compose.prod.yml exec -T db pg_dump -U ecoservices ecoservices | gzip > /opt/backups/ecoservices-$(date +\%F).sql.gz
```
