"""URL-маршрути промосайту.

Сайт статичний, тож усі сторінки — це TemplateView.
Два сайти лежать у власних теках, картинки — спільні в `assets/`:
  old-site/  → попередня версія (aleshin-luxe.html, privacy.html)
  new-site/  → новий корпоративний сайт (aleshin-corporate.html)
"""

from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # --- Старий сайт (головна) --------------------------------------
    path(
        "",
        TemplateView.as_view(template_name="old-site/aleshin-luxe.html"),
        name="home",
    ),
    path(
        "aleshin-luxe.html",
        TemplateView.as_view(template_name="old-site/aleshin-luxe.html"),
    ),
    # --- Новий корпоративний сайт -----------------------------------
    path(
        "corporate",
        TemplateView.as_view(template_name="new-site/aleshin-corporate.html"),
        name="corporate",
    ),
    path(
        "corporate.html",
        TemplateView.as_view(template_name="new-site/aleshin-corporate.html"),
    ),
    # --- Спільні сторінки -------------------------------------------
    path(
        "privacy.html",
        TemplateView.as_view(template_name="old-site/privacy.html"),
        name="privacy",
    ),
    # SEO-файли
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt", content_type="text/plain"
        ),
    ),
    path(
        "sitemap.xml",
        TemplateView.as_view(
            template_name="sitemap.xml", content_type="application/xml"
        ),
    ),
]
