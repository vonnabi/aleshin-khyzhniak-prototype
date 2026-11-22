"""Посадкові сторінки послуг.

Кожна сторінка — модуль у цій теці зі словником PAGE. HTML збирає
`python -m landings.build` (файли лягають у new-site/). Маршрути й sitemap
беруть перелік звідси, тому нову сторінку достатньо додати в MODULES.
"""

from importlib import import_module

MODULES = ["ohd_15_mln"]


def pages():
    return [import_module(f"landings.{name}").PAGE for name in MODULES]


def slugs(published_only=False):
    return [p["slug"] for p in pages() if p.get("published") or not published_only]
