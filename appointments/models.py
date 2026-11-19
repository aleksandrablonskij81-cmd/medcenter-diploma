from django.conf import settings
from django.db import models


class Appointment(models.Model):
    """Запись на приём."""

    STATUS_NEW = "new"
    STATUS_CONFIRMED = "confirmed"
    STATUS_DONE = "done"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_NEW, "Новая"),
        (STATUS_CONFIRMED, "Подтверждена"),
        (STATUS_DONE, "Выполнена"),
        (STATUS_CANCELLED, "Отменена"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Пациент",
    )
    service = models.ForeignKey(
        "services.Service",
        on_delete=models.PROTECT,
        related_name="appointments",
        verbose_name="Услуга",
    )
    date = models.DateField("Дата приёма")
    time = models.TimeField("Время приёма")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "Запись на приём"
        verbose_name_plural = "Записи на приём"
        ordering = ["-date", "-time"]

    def __str__(self):
        return f"{self.user} — {self.service} — {self.date} {self.time:%H:%M}"


class DiagnosticResult(models.Model):
    """Результат диагностики, привязанный к записи."""

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="result",
        verbose_name="Запись",
    )
    conclusion = models.TextField("Заключение")
    file = models.FileField("Файл результата", upload_to="results/", blank=True, null=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Результат диагностики"
        verbose_name_plural = "Результаты диагностики"

    def __str__(self):
        return f"Результат по записи #{self.appointment_id}"