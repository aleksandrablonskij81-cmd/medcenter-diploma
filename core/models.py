from django.db import models


class SiteSettings(models.Model):
    """Настройки сайта — singleton (одна запись)."""

    company_name = models.CharField("Название компании", max_length=255, default="МедЦентр")
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    address = models.CharField("Адрес", max_length=255, blank=True)
    map_embed_url = models.URLField("URL для iframe карты", blank=True)
    about_short = models.TextField("Краткое описание (главная)", blank=True)
    about_history = models.TextField("История компании", blank=True)
    mission = models.TextField("Миссия и ценности", blank=True)
    work_hours = models.CharField("Часы работы", max_length=255, blank=True)

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ContactRequest(models.Model):
    """Заявка с формы обратной связи."""

    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    is_processed = models.BooleanField("Обработана", default=False)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.created_at:%d.%m.%Y %H:%M}"


class Doctor(models.Model):
    """Врач команды."""

    full_name = models.CharField("ФИО", max_length=255)
    specialization = models.CharField("Специализация", max_length=255)
    photo = models.ImageField("Фото", upload_to="doctors/", blank=True, null=True)
    description = models.TextField("Описание", blank=True)
    experience_years = models.PositiveIntegerField("Стаж (лет)", default=0)
    is_active = models.BooleanField("Показывать на сайте", default=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
        ordering = ["order", "full_name"]

    def __str__(self):
        return f"{self.full_name} — {self.specialization}"