"""Заявки із сайту: міні-CRM у адмінці Django.

Статуси й поля відповідають розділу 7 ТЗ: нова → в роботі → консультація →
договір → оплата / відмова; UTM-мітки, дублікати, облік договорів і платежів,
обмеження доступу за практиками (адвокатська таємниця).
"""

import re

from django.conf import settings
from django.db import models

PRACTICES = [
    ("kryminalne", "Кримінальне право"),
    ("viiskove", "Військове право"),
    ("vyplaty", "Військові виплати"),
    ("bronyuvannya", "Бронювання та критичність"),
    ("simejne", "Сімейне право"),
    ("tsyvilne", "Цивільне право"),
    ("korporatyvne", "Захист бізнесу"),
    ("administratyvne", "Адміністративне право"),
    ("migraczijne", "Міграційне право"),
]
PRACTICE_KEYS = {key for key, _ in PRACTICES}


def phone_digits(value):
    """Номер у вигляді самих цифр без коду країни — для пошуку дублікатів."""
    digits = re.sub(r"\D", "", value or "")
    if len(digits) < 9:
        return ""
    return digits[-9:]


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Нова"
        IN_PROGRESS = "in_progress", "В роботі"
        CONSULTATION = "consultation", "Консультація"
        CONTRACT = "contract", "Договір"
        PAID = "paid", "Оплата"
        REFUSED = "refused", "Відмова"

    created_at = models.DateTimeField("створено", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("змінено", auto_now=True)

    name = models.CharField("імʼя", max_length=120)
    contact = models.CharField("телефон або месенджер", max_length=160)
    phone_key = models.CharField(max_length=12, blank=True, db_index=True, editable=False)
    message = models.TextField("звернення", blank=True)

    practice = models.CharField(
        "практика", max_length=32, choices=PRACTICES, blank=True, db_index=True
    )
    status = models.CharField(
        "статус", max_length=16, choices=Status.choices, default=Status.NEW, db_index=True
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="відповідальний",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="leads",
    )
    note = models.TextField("нотатки", blank=True)

    contract_date = models.DateField("дата договору", null=True, blank=True)
    contract_amount = models.DecimalField(
        "сума договору, грн", max_digits=12, decimal_places=2, null=True, blank=True
    )
    paid_amount = models.DecimalField(
        "отримано, грн", max_digits=12, decimal_places=2, null=True, blank=True
    )

    # Звідки прийшла заявка
    page = models.CharField("сторінка форми", max_length=300, blank=True)
    landing = models.CharField("перша сторінка візиту", max_length=300, blank=True)
    referrer = models.CharField("звідки перейшли", max_length=500, blank=True)
    utm_source = models.CharField(max_length=150, blank=True, db_index=True)
    utm_medium = models.CharField(max_length=150, blank=True)
    utm_campaign = models.CharField(max_length=150, blank=True)
    utm_content = models.CharField(max_length=150, blank=True)
    utm_term = models.CharField(max_length=150, blank=True)
    gclid = models.CharField("Google click id", max_length=200, blank=True)
    fbclid = models.CharField("Meta click id", max_length=200, blank=True)

    duplicate_of = models.ForeignKey(
        "self",
        verbose_name="повтор заявки",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="duplicates",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "заявка"
        verbose_name_plural = "заявки"
        permissions = [("view_all_leads", "Бачить заявки всіх практик")]

    def __str__(self):
        return f"№{self.pk} · {self.name}"

    def save(self, *args, **kwargs):
        self.phone_key = phone_digits(self.contact)
        super().save(*args, **kwargs)

    @property
    def source(self):
        if self.utm_source:
            return "/".join(filter(None, [self.utm_source, self.utm_medium]))
        if self.gclid:
            return "google/cpc"
        if self.fbclid:
            return "meta/paid"
        return "прямий або пошук"


class PracticeAccess(models.Model):
    """Які практики бачить користувач. Без записів він бачить лише свої заявки."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="користувач",
        on_delete=models.CASCADE,
        related_name="practice_access",
    )
    practice = models.CharField("практика", max_length=32, choices=PRACTICES)

    class Meta:
        unique_together = [("user", "practice")]
        verbose_name = "доступ до практики"
        verbose_name_plural = "доступи до практик"

    def __str__(self):
        return f"{self.user} → {self.get_practice_display()}"
