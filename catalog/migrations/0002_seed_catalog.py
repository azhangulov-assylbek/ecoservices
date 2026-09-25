"""Начальное наполнение каталога сервисов и оборудования (по утверждённому макету, вариант 3)."""
from django.db import migrations

GROUPS = ["Разрешения и НДТ", "ESG и устойчивое развитие", "Мониторинг и данные", "Отходы", "Отчётность и контроль"]

SERVICES = [
    # группа, slug, название, описание, статус, тема, задачи, featured
    (0, "ndt-check", "Проверка объекта по НДТ",
     "Введите параметры установок и фактические выбросы. Сервис сравнит их с технологическими показателями справочника НДТ и предложит техники для снижения, со ссылками на пункты справочника.",
     "beta", "industry", "ker,tech", True),
    (0, "tech-assessment", "Оценка технологии по критериям НДТ",
     "Проверка новой технологии на соответствие критериям включения в справочник.", "dev", "industry", "tech", False),
    (0, "ker-prep", "Подготовка к КЭР",
     "Чек-лист документов и разрывов до получения комплексного экологического разрешения.", "dev", "industry", "ker", False),
    (0, "ndt-search", "Поиск по справочникам НДТ",
     "Вопрос обычным языком, ответ с цитатой и номером пункта справочника.", "plan", "industry", "ker,tech", False),
    (1, "esg-p5", "ESG-отчёт по стандарту P5",
     "Оценка воздействий проектов на людей, планету и экономику по стандарту PMI–GPM P5: существенные темы, показатели GRI и ISSB, привязка к Целям устойчивого развития.",
     "beta", "partner", "esg,report", True),
    (1, "ghg-inventory", "Инвентаризация парниковых газов",
     "Расчёт выбросов парниковых газов по источникам и видам топлива.", "plan", "climate", "emis,esg", False),
    (2, "monitoring-cabinet", "Кабинет данных мониторинга",
     "Показания датчиков выбросов, воды, пыли и шума в одном месте, с сигналами о превышениях.", "dev", "water", "monitor,report,emis", False),
    (2, "emission-fee", "Калькулятор платы за эмиссии",
     "Расчёт платы за выбросы, сбросы и размещение отходов по актуальным ставкам.", "plan", "climate", "emis,report", False),
    (3, "waste-classifier", "Классификатор отходов",
     "Определение кода отхода и уровня опасности по описанию и составу.", "plan", "industry", "waste", False),
    (3, "waste-passport", "Паспорт опасных отходов",
     "Заполнение паспорта по шаблону с проверкой обязательных полей.", "plan", "industry", "waste,report", False),
    (4, "eco-calendar", "Календарь экологических обязательств",
     "Сроки отчётов, платежей и разрешений по каждому объекту с напоминаниями.", "plan", "partner", "report,ker", False),
    (4, "pek-assistant", "Помощник по программе ПЭК",
     "Структура программы производственного экологического контроля под ваш объект.", "plan", "water", "report,ker,monitor", False),
    (4, "law-monitor", "Мониторинг законодательства",
     "Новые справочники НДТ и изменения законодательства, которые касаются ваших объектов.", "plan", "partner", "report,ker,tech", False),
]

EQUIPMENT = [
    ("Выбросы", "Системы на источниках: дымовые трубы котельных, ТЭЦ, технологических печей.",
     "SO₂, NOx, CO, CO₂, O₂, пыль, температура, давление и расход газов", "climate"),
    ("Качество воды", "Станции и погружные зонды для водоёмов, водозаборов и выпусков сточных вод.",
     "pH, растворённый кислород, электропроводность, мутность, ХПК, аммонийный азот, фосфор", "water"),
    ("Пыль", "Посты для площадок, карьеров, складов сыпучих материалов и границы СЗЗ.",
     "PM2.5, PM10, общая пыль, ветер, температура, влажность", "health"),
    ("Шум", "Автоматические посты для промышленных объектов, дорог и жилой застройки рядом с производством.",
     "Уровни звука в реальном времени, превышения по времени суток", "health"),
]


def seed(apps, schema_editor):
    ServiceGroup = apps.get_model("catalog", "ServiceGroup")
    Service = apps.get_model("catalog", "Service")
    Equipment = apps.get_model("catalog", "Equipment")
    groups = [ServiceGroup.objects.create(name=n, order=i) for i, n in enumerate(GROUPS)]
    for order, (g, slug, name, desc, st, theme, tasks, feat) in enumerate(SERVICES):
        Service.objects.create(group=groups[g], slug=slug, name=name, description=desc, status=st,
                               theme=theme, tasks=tasks, featured=feat, order=order)
    for order, (name, desc, params, theme) in enumerate(EQUIPMENT):
        Equipment.objects.create(name=name, description=desc, parameters=params, theme=theme, order=order)


def unseed(apps, schema_editor):
    for m in ("Service", "ServiceGroup", "Equipment"):
        apps.get_model("catalog", m).objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("catalog", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]
