# Развёртывание ecoservices.kz на AWS Lightsail

Lightsail — простой виртуальный сервер AWS с фиксированной ценой. Проект запускается тем же
`docker-compose.prod.yml` (Django + PostgreSQL + Caddy с автоматическим HTTPS), что и на любом VPS.
Домен остаётся зарегистрированным на hoster.kz, меняются только DNS-записи.

## 0. Аккаунт AWS
1. Зарегистрируйтесь на aws.amazon.com. При выборе плана выберите **Paid plan**:
   кредиты новым клиентам даются и на нём, а аккаунт не закроется через 6 месяцев
   (на Free plan по окончании срока аккаунт закрывается вместе с данными).
   Paid plan также нужен для заявки в AWS Activate (см. раздел 8).
2. Включите двухфакторную аутентификацию (MFA) для root-пользователя.
3. **Billing → Budgets → Create budget**: месячный бюджет, например $10, с уведомлением на почту
   при 80% и 100%. Так вы узнаете о любых расходах заранее.

## 1. Сервер
Lightsail → **Create instance**:
- Регион: **Frankfurt (eu-central-1)** — ближайший к Казахстану с хорошей задержкой.
- Платформа: **Linux/Unix**, образ: **OS Only → Ubuntu 24.04 LTS**.
- Тариф: не меньше **2 ГБ RAM** (PostgreSQL + Django + Caddy + сборка Docker).
  Проверьте, на какие тарифы сейчас действует бесплатный пробный период.
- Имя: `ecoservices`. Нажмите **Create instance**.

## 2. Статический IP и порты
- Вкладка **Networking** сервера → **Attach static IP** → создать и прикрепить.
  Запишите этот IP — он понадобится для DNS.
- Там же, **IPv4 Firewall** → **Add rule** → **HTTPS (443)**.
  Правила SSH (22) и HTTP (80) обычно уже есть.

## 3. DNS на hoster.kz
В панели hoster.kz, в DNS-зоне домена ecoservices.kz:
- A-запись `@` (ecoservices.kz) → статический IP из Lightsail
- A-запись `www` → тот же IP
- Удалите старые A-записи, указывающие на виртуальный хостинг hoster.kz.

Изменения DNS распространяются от нескольких минут до нескольких часов.
Проверка в PowerShell: `nslookup ecoservices.kz` должен показать IP Lightsail.

## 4. Подключение к серверу
Проще всего — кнопка **Connect using SSH** на странице сервера в Lightsail:
терминал откроется прямо в браузере, ключи на Windows настраивать не нужно.

```bash
sudo -i
apt update && apt upgrade -y
# файл подкачки: страхует от нехватки памяти при сборке
fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
# Docker
curl -fsSL https://get.docker.com | sh
```

## 5. Код и настройки
```bash
git clone https://github.com/azhangulov-assylbek/ecoservices.git /opt/ecoservices
cd /opt/ecoservices
cp .env.example .env
python3 -c "import secrets; print(secrets.token_urlsafe(50))"   # скопируйте ключ
nano .env
```
В `.env` заполните `DJANGO_SECRET_KEY`, пароль базы в `POSTGRES_PASSWORD` и тот же пароль
в `DATABASE_URL`. Сохранить в nano: `Ctrl+O`, `Enter`, выйти: `Ctrl+X`.

## 6. Запуск
```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
docker compose -f docker-compose.prod.yml ps
```
Когда DNS начнёт указывать на сервер, Caddy сам получит HTTPS-сертификат.
Сайт: https://ecoservices.kz, админка: https://ecoservices.kz/admin/

Логи при проблемах:
```bash
docker compose -f docker-compose.prod.yml logs --tail=100 web
docker compose -f docker-compose.prod.yml logs --tail=100 caddy
```

## 7. Обновление сайта после git push
```bash
cd /opt/ecoservices && git pull
docker compose -f docker-compose.prod.yml up -d --build
```
Позже это можно автоматизировать через GitHub Actions.

## 8. Резервные копии
- Lightsail → сервер → **Snapshots** → включить автоматические ежедневные снимки
  (небольшая дополнительная плата).
- Дамп базы по расписанию:
```bash
mkdir -p /opt/backups
crontab -e
# добавить строку:
0 3 * * * cd /opt/ecoservices && docker compose -f docker-compose.prod.yml exec -T db pg_dump -U ecoservices ecoservices | gzip > /opt/backups/ecoservices-$(date +\%F).sql.gz
```

## 9. AWS Activate (кредиты для стартапов)
Когда сайт заработает на домене, подайте заявку в **AWS Activate Founders**:
для самофинансируемых стартапов — кредиты AWS без доли в компании.
Условия: аккаунт на Paid plan, работающий сайт компании, лучше корпоративная почта
(например, на домене ecomeken.kz или ecoservices.kz), а не Gmail.
Кредиты можно тратить в том числе на Amazon Bedrock — там доступны модели Claude,
что пригодится для ИИ-модуля сервисов.

## Важно про данные
Регионов AWS в Казахстане нет. Для демо и первых заявок это приемлемо; перед работой
с реальными клиентскими данными нужно решить вопрос хранения персональных данных в РК
(например, перенос базы на казахстанский сервер).
