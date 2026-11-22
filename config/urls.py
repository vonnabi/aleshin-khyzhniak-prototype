"""URL-маршрути промосайту.

Сайт статичний, тож усі сторінки — це TemplateView.
Два сайти лежать у власних теках, картинки — спільні в `assets/`:
  old-site/  → попередня версія (aleshin-luxe.html, privacy.html)
  new-site/  → новий корпоративний сайт та його внутрішні сторінки
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from config.seo import robots_txt, sitemap_xml
from landings import slugs as landing_slugs
from leads.views import create_lead

# Що відкривається на головній адресі: старий сайт або новий (після запуску).
HOME_TEMPLATE = (
    "new-site/aleshin-corporate.html"
    if settings.NEW_SITE_AT_ROOT
    else "old-site/aleshin-luxe.html"
)

urlpatterns = [
    # --- Заявки: приймання з форм і облік ---------------------------
    path("api/lead/", create_lead, name="create_lead"),
    path("crm/", admin.site.urls),
    path(
        "thank-you.html",
        TemplateView.as_view(template_name="new-site/thank-you.html"),
        name="thank_you",
    ),
    # --- Старий сайт (головна) --------------------------------------
    path(
        "",
        TemplateView.as_view(template_name=HOME_TEMPLATE),
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
        "brandbook/",
        TemplateView.as_view(template_name="brandbook/brandbook.html"),
        name="brandbook",
    ),
    path(
        "brandbook.html",
        TemplateView.as_view(template_name="brandbook/brandbook.html"),
    ),
    # Попередня головна — збережена до погодження нового варіанта
    path(
        "home-old.html",
        TemplateView.as_view(template_name="new-site/home-old.html"),
        name="home_old",
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
    # --- Детальні сторінки практик ---
    *[
        path(
            f"practice-{slug}.html",
            TemplateView.as_view(
                template_name=f"new-site/practice-{slug}.html"
            ),
            name=f"practice_{slug}",
        )
        for slug in (
            "kryminalne",
            "administratyvne",
            "tsyvilne",
            "simejne",
            "korporatyvne",
            "migraczijne",
            "viiskove",
        )
    ],
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
        "case-detail.html",
        TemplateView.as_view(template_name="new-site/case-detail.html"),
        name="case_detail",
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
        "home-rebuild.css",
        TemplateView.as_view(
            template_name="new-site/home-rebuild.css", content_type="text/css"
        ),
        name="corporate_home_styles",
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
    # --- Посадкові сторінки послуг (перелік — у landings/) -----------
    *[
        path(
            f"{slug}.html",
            TemplateView.as_view(template_name=f"new-site/{slug}.html"),
            name=f"landing_{slug}",
        )
        for slug in landing_slugs()
    ],
    path("robots.txt", robots_txt),
    path("sitemap.xml", sitemap_xml),
]
