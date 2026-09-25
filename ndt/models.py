"""База справочников НДТ — ключевой актив продукта.

Технологические показатели вносятся ТОЛЬКО из официальных текстов справочников
(adilet.zan.kz) с указанием пункта/таблицы, чтобы каждый вывод сервиса можно было проверить.
"""
from django.db import models


class Reference(models.Model):
    title = models.CharField("Название справочника", max_length=300)
    act = models.CharField("Нормативный акт", max_length=200, help_text="Например: ПП РК от 23.01.2024 № 23")
    adopted = models.DateField("Дата утверждения", null=True, blank=True)
    source_url = models.URLField("Ссылка на официальный текст", blank=True)
    is_active = models.BooleanField("Действующий", default=True)
    notes = models.TextField("Примечания", blank=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Справочник НДТ"
        verbose_name_plural = "Справочники НДТ"

    def __str__(self):
        return self.title


class Technique(models.Model):
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, related_name="techniques", verbose_name="Справочник")
    code = models.CharField("Номер НДТ", max_length=30, blank=True)
    name = models.CharField("Наименование техники", max_length=300)
    description = models.TextField("Описание", blank=True)
    pollutants = models.CharField("Вещества, на которые влияет", max_length=200, blank=True)
    section = models.CharField("Пункт справочника", max_length=60, blank=True)

    class Meta:
        ordering = ["reference", "code"]
        verbose_name = "Техника НДТ"
        verbose_name_plural = "Техники НДТ"

    def __str__(self):
        return f"{self.code} {self.name}".strip()


class EmissionLimit(models.Model):
    """Технологический показатель (уровень эмиссий, связанный с НДТ)."""
    class Medium(models.TextChoices):
        AIR = "air", "Атмосферный воздух"
        WATER = "water", "Сбросы в воду"

    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, related_name="limits", verbose_name="Справочник")
    medium = models.CharField("Среда", max_length=6, choices=Medium.choices, default=Medium.AIR)
    pollutant = models.CharField("Загрязняющее вещество", max_length=80)
    fuel = models.CharField("Топливо / сырьё", max_length=120, blank=True)
    installation = models.CharField("Тип установки", max_length=200, blank=True)
    capacity_min = models.FloatField("Мощность от, МВт", null=True, blank=True)
    capacity_max = models.FloatField("Мощность до, МВт", null=True, blank=True)
    is_new_plant = models.BooleanField("Для новых установок", null=True, blank=True)
    value_min = models.FloatField("Значение от", null=True, blank=True)
    value_max = models.FloatField("Значение до", null=True, blank=True)
    unit = models.CharField("Единица", max_length=30, default="мг/нм³")
    averaging = models.CharField("Период усреднения", max_length=60, blank=True)
    o2_reference = models.CharField("Приведение к O₂", max_length=20, blank=True)
    section = models.CharField("Таблица / пункт справочника", max_length=60,
                               help_text="Обязательно: где в официальном тексте находится значение")
    verified = models.BooleanField("Сверено с официальным текстом", default=False)

    class Meta:
        ordering = ["reference", "pollutant", "fuel", "capacity_min"]
        verbose_name = "Технологический показатель"
        verbose_name_plural = "Технологические показатели"

    def __str__(self):
        rng = f"{self.value_min or ''}–{self.value_max or ''}".strip("–")
        return f"{self.pollutant}, {self.fuel or 'все виды'}: {rng} {self.unit}"
