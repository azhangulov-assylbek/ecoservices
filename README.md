# ecoservices.kz

Цифровые сервисы для устойчивого развития предприятий: соответствие НДТ, ESG-отчётность по стандарту P5,
оборудование для мониторинга выбросов, воды, пыли и шума. Проект ТОО «ЭКОМЕКЕН».

## Быстрый старт
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Сайт: http://localhost:8000, админка: http://localhost:8000/admin/

Или через Docker: `docker compose up --build`.

## Документация
- `CLAUDE.md` — правила проекта для Claude Code
- `docs/roadmap.md` — дорожная карта MVP
- `docs/decisions.md` — принятые решения
- `docs/deploy-aws-lightsail.md` — развёртывание на AWS Lightsail (основной вариант)
- `docs/deploy-hoster-kz.md` — развёртывание на VPS hoster.kz (запасной вариант)
- `docs/first-prompt.md` — первые промпты для Claude Code
