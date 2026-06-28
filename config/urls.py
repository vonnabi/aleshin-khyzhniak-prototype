"""URL-маршрути промосайту.

Сайт статичний, тож усі сторінки — це TemplateView.
Шляхи збігаються з відносними посиланнями у HTML
(`aleshin-luxe.html`, `privacy.html`), тому верстку правити не довелося.
"""

from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # Головна
    path("", TemplateView.as_view(template_name="aleshin-luxe.html"), name="home"),
    path(
        "aleshin-luxe.html",
        TemplateView.as_view(template_name="aleshin-luxe.html"),
    ),
    # Політика конфіденційності
    path(
        "privacy.html",
        TemplateView.as_view(template_name="privacy.html"),
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
