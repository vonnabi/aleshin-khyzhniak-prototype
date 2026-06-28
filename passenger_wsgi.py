"""Точка входу для cPanel / Phusion Passenger.

cPanel «Setup Python App» шукає саме цей файл і викликає змінну `application`.
"""

import os
import sys

# Додаємо корінь проєкту у sys.path, щоб імпортувався пакет config/.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application  # noqa: E402
