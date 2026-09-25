from django.db import models


class Theme(models.TextChoices):
    """Тематические цвета, связанные с ЦУР (см. блок «Вклад в ЦУР» на главной)."""
    CLIMATE = "climate", "Климат (ЦУР 7, 13)"
    WATER = "water", "Вода (ЦУР 6, 14)"
    INDUSTRY = "industry", "Производство (ЦУР 9, 12)"
    HEALTH = "health", "Здоровье и города (ЦУР 3, 11)"
    PARTNER = "partner", "Отчётность (ЦУР 8, 17)"


class ServiceGroup(models.Model):
    name = models.CharField("Название группы", max_length=120)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Группа сервисов"
        verbose_name_plural = "Группы сервисов"

    def __str__(self):
        return self.name


class Service(models.Model):
    class Status(models.TextChoices):
        BETA = "beta", "Бета"
        DEV = "dev", "В разработке"
        PLAN = "plan", "Планируется"

    # Задачи пользователя для фильтра на главной (ключи совпадают с data-task кнопок)
    TASKS = {
        "ker": "Получить или пересмотреть КЭР",
        "esg": "Подготовить ESG-отчёт",
        "monitor": "Организовать мониторинг",
        "tech": "Внедрить новую технологию",
        "waste": "Разобраться с отходами",
        "emis": "Посчитать выбросы и платежи",
        "report": "Сдать отчётность вовремя",
    }

    group = models.ForeignKey(ServiceGroup, on_delete=models.PROTECT, related_name="services", verbose_name="Группа")
    name = models.CharField("Название", max_length=160)
    slug = models.SlugField(unique=True)
    description = models.TextField("Краткое описание")
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
    description = models.TextField("Описание")
    parameters = models.CharField("Измеряемые параметры", max_length=300)
    theme = models.CharField("Тема ЦУР", max_length=12, choices=Theme.choices)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Направление оборудования"
        verbose_name_plural = "Оборудование"

    def __str__(self):
        return self.name


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
