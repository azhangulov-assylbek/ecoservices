from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

# Языки, для которых у переводимых полей каталога есть отдельные колонки (name_kk, name_en, ...).
# Русский — основной язык, для него отдельной колонки нет: это сами поля name/description/parameters.
TRANSLATABLE_LANGUAGES = ["kk", "en"]


def localized_field(instance, field):
    """Значение поля на текущем активном языке с откатом на русский, если перевод не заполнен.

    Используется вместо django-modeltranslation: переводы — обычные CharField/TextField
    (`<field>_kk`, `<field>_en`), которые видно и редактируется прямо в админке.
    """
    lang = get_language()
    if lang in TRANSLATABLE_LANGUAGES:
        value = getattr(instance, f"{field}_{lang}", "")
        if value:
            return value
    return getattr(instance, field)


class Theme(models.TextChoices):
    """Тематические цвета, связанные с ЦУР (см. блок «Вклад в ЦУР» на главной)."""
    CLIMATE = "climate", _("Климат (ЦУР 7, 13)")
    WATER = "water", _("Вода (ЦУР 6, 14)")
    INDUSTRY = "industry", _("Производство (ЦУР 9, 12)")
    HEALTH = "health", _("Здоровье и города (ЦУР 3, 11)")
    PARTNER = "partner", _("Отчётность (ЦУР 8, 17)")


class ServiceGroup(models.Model):
    name = models.CharField("Название группы", max_length=120)
    name_kk = models.CharField("Название группы (kk)", max_length=120, blank=True)
    name_en = models.CharField("Название группы (en)", max_length=120, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Группа сервисов"
        verbose_name_plural = "Группы сервисов"

    def __str__(self):
        return self.name

    @property
    def display_name(self):
        return localized_field(self, "name")


class Service(models.Model):
    class Status(models.TextChoices):
        BETA = "beta", _("Бета")
        DEV = "dev", _("В разработке")
        PLAN = "plan", _("Планируется")

    # Задачи пользователя для фильтра на главной (ключи совпадают с data-task кнопок)
    TASKS = {
        "ker": _("Получить или пересмотреть КЭР"),
        "esg": _("Подготовить ESG-отчёт"),
        "monitor": _("Организовать мониторинг"),
        "tech": _("Внедрить новую технологию"),
        "waste": _("Разобраться с отходами"),
        "emis": _("Посчитать выбросы и платежи"),
        "report": _("Сдать отчётность вовремя"),
    }

    group = models.ForeignKey(ServiceGroup, on_delete=models.PROTECT, related_name="services", verbose_name="Группа")
    name = models.CharField("Название", max_length=160)
    name_kk = models.CharField("Название (kk)", max_length=160, blank=True)
    name_en = models.CharField("Название (en)", max_length=160, blank=True)
    slug = models.SlugField(unique=True)
    description = models.TextField("Краткое описание")
    description_kk = models.TextField("Краткое описание (kk)", blank=True)
    description_en = models.TextField("Краткое описание (en)", blank=True)
    status = models.CharField("Статус", max_length=8, choices=Status.choices, default=Status.PLAN)
    theme = models.CharField("Тема ЦУР", max_length=12, choices=Theme.choices)
    tasks = models.CharField("Задачи (ключи через запятую)", max_length=200, blank=True,
                             help_text="Например: ker,tech. Допустимые ключи: " + ", ".join(TASKS))
    featured = models.BooleanField("Показывать крупно на главной", default=False)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["group__order", "order", "name"]
        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"

    def __str__(self):
        return self.name

    @property
    def task_list(self):
        return [t.strip() for t in self.tasks.split(",") if t.strip()]

    @property
    def display_name(self):
        return localized_field(self, "name")

    @property
    def display_description(self):
        return localized_field(self, "description")


class NotifyRequest(models.Model):
    """Подписка «Сообщить о запуске» — показывает спрос на будущие сервисы."""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="notify_requests")
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подписка на запуск"
        verbose_name_plural = "Подписки на запуск"
        unique_together = ("service", "email")


class Equipment(models.Model):
    name = models.CharField("Название", max_length=120)
    name_kk = models.CharField("Название (kk)", max_length=120, blank=True)
    name_en = models.CharField("Название (en)", max_length=120, blank=True)
    description = models.TextField("Описание")
    description_kk = models.TextField("Описание (kk)", blank=True)
    description_en = models.TextField("Описание (en)", blank=True)
    parameters = models.CharField("Измеряемые параметры", max_length=300)
    parameters_kk = models.CharField("Измеряемые параметры (kk)", max_length=300, blank=True)
    parameters_en = models.CharField("Измеряемые параметры (en)", max_length=300, blank=True)
    theme = models.CharField("Тема ЦУР", max_length=12, choices=Theme.choices)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Направление оборудования"
        verbose_name_plural = "Оборудование"

    def __str__(self):
        return self.name

    @property
    def display_name(self):
        return localized_field(self, "name")

    @property
    def display_description(self):
        return localized_field(self, "description")

    @property
    def display_parameters(self):
        return localized_field(self, "parameters")


class QuoteRequest(models.Model):
    """Заявка на коммерческое предложение по оборудованию."""
    class State(models.TextChoices):
        NEW = "new", "Новая"
        IN_WORK = "work", "В работе"
        DONE = "done", "Закрыта"

    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Оборудование")
    company = models.CharField("Компания", max_length=200)
    contact = models.CharField("Телефон или email", max_length=200)
    task = models.TextField("Объект и задача", blank=True)
    state = models.CharField("Статус", max_length=6, choices=State.choices, default=State.NEW)
    created = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Заявка на оборудование"
        verbose_name_plural = "Заявки на оборудование"

    def __str__(self):
        return f"{self.company} — {self.equipment or 'без категории'}"
