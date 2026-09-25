"""Переводы (kk/en) для каталога, наполненного в 0002_seed_catalog."""
from django.db import migrations

GROUPS_TRANSLATIONS = {
    # name_ru: (name_kk, name_en)
    "Разрешения и НДТ": ("Рұқсаттар және ЕҮҚТ", "Permits and BAT"),
    "ESG и устойчивое развитие": ("ESG және орнықты даму", "ESG and sustainable development"),
    "Мониторинг и данные": ("Мониторинг және деректер", "Monitoring and data"),
    "Отходы": ("Қалдықтар", "Waste"),
    "Отчётность и контроль": ("Есептілік және бақылау", "Reporting and control"),
}

SERVICES_TRANSLATIONS = {
    # slug: (name_kk, name_en, description_kk, description_en)
    "ndt-check": (
        "Объектіні ЕҮҚТ бойынша тексеру",
        "BAT compliance check",
        "Қондырғылардың параметрлері мен нақты шығарындыларды енгізіңіз. Сервис оларды ЕҮҚТ "
        "анықтамалығының технологиялық көрсеткіштерімен салыстырып, анықтамалық тармақтарына "
        "сілтеме бере отырып, азайту техникаларын ұсынады.",
        "Enter your installation parameters and actual emissions. The service compares them with "
        "the BAT reference document's technological indicators and suggests reduction techniques, "
        "with references to the relevant sections.",
    ),
    "tech-assessment": (
        "Технологияны ЕҮҚТ критерийлері бойынша бағалау",
        "Technology assessment against BAT criteria",
        "Жаңа технологияны анықтамалыққа енгізу критерийлеріне сәйкестігін тексеру.",
        "Checking whether a new technology meets the criteria for inclusion in the reference document.",
    ),
    "ker-prep": (
        "КЭР-ге дайындық",
        "Preparing for an Integrated Environmental Permit (IEP)",
        "Кешенді экологиялық рұқсат алуға дейінгі құжаттар мен олқылықтардың тексеру парағы.",
        "A checklist of documents and gaps before obtaining an integrated environmental permit.",
    ),
    "ndt-search": (
        "ЕҮҚТ анықтамалықтары бойынша іздеу",
        "Search across BAT reference documents",
        "Сұрақты қарапайым тілде қойыңыз — жауап анықтамалықтың тармақ нөмірі мен дәйексөзімен келеді.",
        "Ask a question in plain language — get an answer with a quote and the reference section number.",
    ),
    "esg-p5": (
        "P5 стандарты бойынша ESG-есебі",
        "ESG report under the P5 standard",
        "Жобалардың адамдарға, планетаға және экономикаға әсерін PMI–GPM P5 стандарты бойынша "
        "бағалау: елеулі тақырыптар, GRI және ISSB көрсеткіштері, Орнықты даму мақсаттарымен байланыс.",
        "Assessing project impacts on people, planet and prosperity under the PMI–GPM P5 standard: "
        "material topics, GRI and ISSB indicators, and links to the Sustainable Development Goals.",
    ),
    "ghg-inventory": (
        "Жылыжай газдарының түгендеуі",
        "Greenhouse gas inventory",
        "Жылыжай газдарының шығарындыларын көздер және отын түрлері бойынша есептеу.",
        "Calculating greenhouse gas emissions by source and fuel type.",
    ),
    "monitoring-cabinet": (
        "Мониторинг деректерінің кабинеті",
        "Monitoring data dashboard",
        "Шығарындылар, су, шаң және шу датчиктерінің көрсеткіштері бір жерде, шектен асу туралы "
        "сигналдармен.",
        "Emissions, water, dust and noise sensor readings in one place, with alerts on exceedances.",
    ),
    "emission-fee": (
        "Эмиссия үшін төлемді есептеу калькуляторы",
        "Emission fee calculator",
        "Шығарындылар, төгінділер және қалдықтарды орналастыру үшін төлемді қолданыстағы ставкалар "
        "бойынша есептеу.",
        "Calculating fees for emissions, discharges and waste disposal at current rates.",
    ),
    "waste-classifier": (
        "Қалдықтар классификаторы",
        "Waste classifier",
        "Сипаттамасы мен құрамы бойынша қалдық кодын және қауіптілік деңгейін анықтау.",
        "Determining the waste code and hazard level from its description and composition.",
    ),
    "waste-passport": (
        "Қауіпті қалдықтар паспорты",
        "Hazardous waste passport",
        "Міндетті өрістерді тексере отырып, паспортты үлгі бойынша толтыру.",
        "Filling out the passport from a template, with validation of required fields.",
    ),
    "eco-calendar": (
        "Экологиялық міндеттемелер күнтізбесі",
        "Environmental obligations calendar",
        "Әрбір объект бойынша есептер, төлемдер және рұқсаттардың мерзімдері, еске салғыштармен.",
        "Deadlines for reports, payments and permits for each site, with reminders.",
    ),
    "pek-assistant": (
        "ӨЭБ бағдарламасы бойынша көмекші",
        "Industrial Environmental Control (IEC) programme assistant",
        "Сіздің объектіңізге арналған өндірістік экологиялық бақылау бағдарламасының құрылымы.",
        "The structure of an industrial environmental control programme tailored to your site.",
    ),
    "law-monitor": (
        "Заңнама мониторингі",
        "Legislation monitoring",
        "Сіздің объектілеріңізге қатысты жаңа ЕҮҚТ анықтамалықтары мен заңнамадағы өзгерістер.",
        "New BAT reference documents and legislative changes relevant to your sites.",
    ),
}

EQUIPMENT_TRANSLATIONS = {
    # name_ru: (name_kk, name_en, description_kk, description_en, parameters_kk, parameters_en)
    "Выбросы": (
        "Шығарындылар",
        "Emissions",
        "Көздердегі жүйелер: қазандықтардың, ЖЭО-ның, технологиялық пештердің түтін мұржалары.",
        "Source-based systems: chimneys of boiler houses, CHP plants, and process furnaces.",
        "SO₂, NOx, CO, CO₂, O₂, шаң, температура, қысым және газ шығыны",
        "SO₂, NOx, CO, CO₂, O₂, dust, temperature, pressure and gas flow",
    ),
    "Качество воды": (
        "Су сапасы",
        "Water quality",
        "Су айдындары, су алу орындары және ағынды суларды шығару үшін станциялар мен батыру "
        "зондтары.",
        "Stations and submersible probes for water bodies, water intakes and wastewater outfalls.",
        "pH, еріген оттегі, электрөткізгіштік, лайлылық, ХҚБ, аммонийлі азот, фосфор",
        "pH, dissolved oxygen, conductivity, turbidity, COD, ammonium nitrogen, phosphorus",
    ),
    "Пыль": (
        "Шаң",
        "Dust",
        "Алаңдар, карьерлер, сусымалы материалдар қоймалары және санитарлық-қорғау аймағы "
        "шекарасы үшін бекеттер.",
        "Monitoring posts for sites, quarries, bulk material storage yards and the sanitary "
        "protection zone boundary.",
        "PM2.5, PM10, жалпы шаң, жел, температура, ылғалдылық",
        "PM2.5, PM10, total dust, wind, temperature, humidity",
    ),
    "Шум": (
        "Шу",
        "Noise",
        "Өндірістік объектілер, жолдар және өндіріске жақын тұрғын үй құрылысы үшін автоматты "
        "бекеттер.",
        "Automatic monitoring posts for industrial facilities, roads and residential areas near "
        "production sites.",
        "Нақты уақыттағы дыбыс деңгейлері, тәулік уақыты бойынша шектен асулар",
        "Real-time sound levels, time-of-day exceedances",
    ),
}


def translate(apps, schema_editor):
    ServiceGroup = apps.get_model("catalog", "ServiceGroup")
    Service = apps.get_model("catalog", "Service")
    Equipment = apps.get_model("catalog", "Equipment")

    for group in ServiceGroup.objects.all():
        kk, en = GROUPS_TRANSLATIONS.get(group.name, ("", ""))
        group.name_kk, group.name_en = kk, en
        group.save(update_fields=["name_kk", "name_en"])

    for service in Service.objects.all():
        kk, en, desc_kk, desc_en = SERVICES_TRANSLATIONS.get(service.slug, ("", "", "", ""))
        service.name_kk, service.name_en = kk, en
        service.description_kk, service.description_en = desc_kk, desc_en
        service.save(update_fields=["name_kk", "name_en", "description_kk", "description_en"])

    for equipment in Equipment.objects.all():
        kk, en, desc_kk, desc_en, params_kk, params_en = EQUIPMENT_TRANSLATIONS.get(
            equipment.name, ("", "", "", "", "", "")
        )
        equipment.name_kk, equipment.name_en = kk, en
        equipment.description_kk, equipment.description_en = desc_kk, desc_en
        equipment.parameters_kk, equipment.parameters_en = params_kk, params_en
        equipment.save(update_fields=[
            "name_kk", "name_en", "description_kk", "description_en", "parameters_kk", "parameters_en",
        ])


def untranslate(apps, schema_editor):
    ServiceGroup = apps.get_model("catalog", "ServiceGroup")
    Service = apps.get_model("catalog", "Service")
    Equipment = apps.get_model("catalog", "Equipment")
    ServiceGroup.objects.update(name_kk="", name_en="")
    Service.objects.update(name_kk="", name_en="", description_kk="", description_en="")
    Equipment.objects.update(
        name_kk="", name_en="", description_kk="", description_en="", parameters_kk="", parameters_en="",
    )


class Migration(migrations.Migration):
    dependencies = [("catalog", "0003_add_translation_fields")]
    operations = [migrations.RunPython(translate, untranslate)]
