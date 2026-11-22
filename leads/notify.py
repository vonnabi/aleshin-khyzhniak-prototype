"""Сповіщення про нову заявку в Telegram.

Працює, лише якщо задано TELEGRAM_BOT_TOKEN і TELEGRAM_CHAT_ID. Текст звернення
за замовчуванням не надсилається: це адвокатська таємниця, його читають у CRM.
"""

import json
import logging
import threading
import urllib.request

from django.conf import settings

log = logging.getLogger("leads")


def _send(text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    body = json.dumps(
        {"chat_id": settings.TELEGRAM_CHAT_ID, "text": text, "disable_web_page_preview": True}
    ).encode()
    request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(request, timeout=8).read()
    except Exception as error:  # сповіщення не повинно ламати приймання заявки
        log.warning("Telegram: не вдалося надіслати сповіщення: %s", error)


def lead_text(lead):
    lines = [
        f"Нова заявка №{lead.pk}",
        f"Імʼя: {lead.name}",
        f"Контакт: {lead.contact}",
        f"Практика: {lead.get_practice_display() or 'не визначено'}",
        f"Джерело: {lead.source}",
    ]
    if lead.duplicate_of_id:
        lines.append(f"Повтор заявки №{lead.duplicate_of_id}")
    if settings.TELEGRAM_INCLUDE_MESSAGE and lead.message:
        lines.append(f"Звернення: {lead.message[:600]}")
    if settings.SITE_URL:
        lines.append(f"{settings.SITE_URL}/crm/leads/lead/{lead.pk}/change/")
    return "\n".join(lines)


def notify_new_lead(lead):
    if not (settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID):
        return False
    threading.Thread(target=_send, args=(lead_text(lead),), daemon=True).start()
    return True
