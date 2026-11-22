"""Приймання заявки з форми сайту."""

import json
from datetime import timedelta
from urllib.parse import urlparse

from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import PRACTICE_KEYS, Lead, phone_digits
from .notify import notify_new_lead

RATE_LIMIT = 6  # заявок з однієї адреси
RATE_WINDOW = 600  # за стільки секунд
DUPLICATE_DAYS = 30
THANK_YOU_URL = "/thank-you.html"

TRACKING_FIELDS = (
    "page", "landing", "referrer", "utm_source", "utm_medium", "utm_campaign",
    "utm_content", "utm_term", "gclid", "fbclid",
)


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return forwarded.split(",")[0].strip() or request.META.get("REMOTE_ADDR", "")


def _practice_from(data):
    practice = (data.get("practice") or "").strip()
    if practice in PRACTICE_KEYS:
        return practice
    page = data.get("page") or ""
    for key in PRACTICE_KEYS:
        if f"practice-{key}" in page:
            return key
    return ""


def _clip(value, limit):
    return str(value or "").strip()[:limit]


@csrf_exempt  # форма стоїть на статичних сторінках; замість токена — перевірка джерела нижче
@require_POST
def create_lead(request):
    origin = request.headers.get("Origin")
    if origin and urlparse(origin).netloc != request.get_host():
        return JsonResponse({"ok": False, "error": "origin"}, status=403)

    if request.content_type == "application/json":
        try:
            data = json.loads(request.body.decode("utf-8") or "{}")
        except (ValueError, UnicodeDecodeError):
            return JsonResponse({"ok": False, "error": "format"}, status=400)
        if not isinstance(data, dict):
            return JsonResponse({"ok": False, "error": "format"}, status=400)
    else:
        data = request.POST.dict()

    # Пастка для ботів: людина це поле не бачить і не заповнює.
    if _clip(data.get("website"), 10):
        return JsonResponse({"ok": True, "redirect": THANK_YOU_URL})

    key = f"lead-rate:{_client_ip(request)}"
    sent = cache.get(key, 0)
    if sent >= RATE_LIMIT:
        return JsonResponse({"ok": False, "error": "rate"}, status=429)
    cache.set(key, sent + 1, RATE_WINDOW)

    name = _clip(data.get("name"), 120)
    contact = _clip(data.get("contact"), 160)
    if not contact or len(contact) < 5:
        return JsonResponse(
            {"ok": False, "error": "contact", "message": "Вкажіть телефон або Telegram."},
            status=400,
        )

    lead = Lead(
        name=name or "Без імені",
        contact=contact,
        message=_clip(data.get("message"), 4000),
        practice=_practice_from(data),
    )
    for field in TRACKING_FIELDS:
        limit = Lead._meta.get_field(field).max_length
        setattr(lead, field, _clip(data.get(field), limit))

    phone = phone_digits(contact)
    if phone:
        since = timezone.now() - timedelta(days=DUPLICATE_DAYS)
        earlier = (
            Lead.objects.filter(phone_key=phone, created_at__gte=since)
            .order_by("created_at")
            .first()
        )
        if earlier:
            lead.duplicate_of = earlier.duplicate_of or earlier
    lead.save()
    notify_new_lead(lead)
    return JsonResponse({"ok": True, "redirect": THANK_YOU_URL})
