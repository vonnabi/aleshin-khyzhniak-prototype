"""URL-маршрути промосайту.

Сайт статичний, тож усі сторінки — це TemplateView.
Два сайти лежать у власних теках, картинки — спільні в `assets/`:
  old-site/  → попередня версія (aleshin-luxe.html, privacy.html)
  new-site/  → новий корпоративний сайт та його внутрішні сторінки
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
    path(
        "aleshin-corporate.html",
        TemplateView.as_view(template_name="new-site/aleshin-corporate.html"),
        name="corporate_legacy_filename",
    ),
    path(
        "about.html",
        TemplateView.as_view(template_name="new-site/about.html"),
        name="about",
    ),
    path(
        "practices.html",
        TemplateView.as_view(template_name="new-site/practices.html"),
        name="practices",
    ),
    path(
        "team.html",
        TemplateView.as_view(template_name="new-site/team.html"),
        name="team",
    ),
    path(
        "cases.html",
        TemplateView.as_view(template_name="new-site/cases.html"),
        name="cases",
    ),
    path(
        "media.html",
        TemplateView.as_view(template_name="new-site/media.html"),
        name="media",
    ),
    path(
        "careers.html",
        TemplateView.as_view(template_name="new-site/careers.html"),
        name="careers",
    ),
    path(
        "contact.html",
        TemplateView.as_view(template_name="new-site/contact.html"),
        name="contact",
    ),
    path(
        "site.css",
        TemplateView.as_view(
            template_name="new-site/site.css", content_type="text/css"
        ),
        name="corporate_styles",
    ),
    path(
        "site.js",
        TemplateView.as_view(
            template_name="new-site/site.js",
            content_type="application/javascript",
        ),
        name="corporate_script",
    ),
    path(
        "privacy.html",
        TemplateView.as_view(template_name="new-site/privacy.html"),
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
