"""SEO-основа: canonical, Open Graph, Schema.org, sitemap.xml і robots.txt.

Сторінки сайту — звичайні HTML-файли без адреси сайту всередині. Усе, що
залежить від домену, додається тут, тому зміна домену — це одна змінна
оточення SITE_URL.
"""

import json
import re
from html import escape

from django.conf import settings
from django.http import HttpResponse

HOME_ALIASES = ("/corporate", "/corporate.html", "/aleshin-corporate.html")

# (шлях, як часто змінюється, вага) — те, що потрапляє в sitemap.xml
SITEMAP_PAGES = [
    ("HOME", "weekly", "1.0"),
    ("/practices.html", "monthly", "0.9"),
    ("/practice-kryminalne.html", "monthly", "0.8"),
    ("/practice-viiskove.html", "monthly", "0.8"),
    ("/practice-tsyvilne.html", "monthly", "0.8"),
    ("/practice-simejne.html", "monthly", "0.8"),
    ("/practice-korporatyvne.html", "monthly", "0.8"),
    ("/practice-administratyvne.html", "monthly", "0.8"),
    ("/practice-migraczijne.html", "monthly", "0.8"),
    ("/about.html", "monthly", "0.7"),
    ("/team.html", "monthly", "0.7"),
    ("/cases.html", "weekly", "0.7"),
    ("/media.html", "weekly", "0.5"),
    ("/contact.html", "yearly", "0.6"),
    ("/careers.html", "monthly", "0.3"),
]
NO_CANONICAL = ("/crm/", "/api/", "/brandbook", "/aleshin-luxe.html")
SHARE_IMAGE = "/assets/team/team-four.jpg"
ORGANIZATION_PAGES = ("HOME", "/about.html", "/contact.html", "/team.html")


def home_path():
    return "/" if settings.NEW_SITE_AT_ROOT else "/corporate"


def base_url(request):
    return settings.SITE_URL or f"{request.scheme}://{request.get_host()}"


def canonical_path(request):
    path = request.path
    if path in HOME_ALIASES or (path == "/" and settings.NEW_SITE_AT_ROOT):
        return home_path()
    if path == "/case-detail.html" and request.GET.get("id"):
        return f"{path}?id={request.GET['id']}"
    return path


def organization(base):
    return {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "name": "Адвокатське обʼєднання «Альошин, Хижняк та Партнери»",
        "alternateName": "Aleshin, Khyzhniak & Partners",
        "url": base + home_path(),
        "logo": base + "/assets/brand/ak-logo.png",
        "image": base + SHARE_IMAGE,
        "telephone": "+380994000303",
        "email": "aleshin.partners@ukr.net",
        "areaServed": {"@type": "Country", "name": "Україна"},
        "sameAs": ["https://www.instagram.com/aleshin_khyzhniak_/"],
    }


class SeoHeadMiddleware:
    """Додає в <head> сторінок нового сайту теги, що залежать від домену."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path
        if (
            request.method != "GET"
            or response.status_code != 200
            or not response.get("Content-Type", "").startswith("text/html")
            or path.startswith(NO_CANONICAL)
            or (path == "/" and not settings.NEW_SITE_AT_ROOT)
        ):
            return response
        html = response.content.decode(response.charset or "utf-8")
        if 'rel="canonical"' in html or "</head>" not in html:
            return response

        base = base_url(request)
        url = base + canonical_path(request)
        title = re.search(r"<title>(.*?)</title>", html, re.S)
        description = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
        tags = [f'<link rel="canonical" href="{escape(url)}">']
        tags += [
            '<meta property="og:type" content="website">',
            '<meta property="og:locale" content="uk_UA">',
            '<meta property="og:site_name" content="Альошин, Хижняк та Партнери">',
            f'<meta property="og:url" content="{escape(url)}">',
            f'<meta property="og:image" content="{escape(base + SHARE_IMAGE)}">',
            '<meta name="twitter:card" content="summary_large_image">',
        ]
        if title:
            tags.append(f'<meta property="og:title" content="{escape(title.group(1).strip())}">')
        if description:
            tags.append(f'<meta property="og:description" content="{description.group(1)}">')
        key = "HOME" if canonical_path(request) == home_path() else path
        if key in ORGANIZATION_PAGES:
            data = json.dumps(organization(base), ensure_ascii=False)
            tags.append(f'<script type="application/ld+json">{data}</script>')
        html = html.replace("</head>", "".join(tags) + "</head>", 1)
        response.content = html.encode(response.charset or "utf-8")
        if response.has_header("Content-Length"):
            response["Content-Length"] = str(len(response.content))
        return response


def robots_txt(request):
    lines = ["User-agent: *", "Allow: /", "Disallow: /crm/", "Disallow: /api/",
             "Disallow: /thank-you.html", "", f"Sitemap: {base_url(request)}/sitemap.xml", ""]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    base = base_url(request)
    items = []
    from landings import slugs

    landing_pages = [(f"/{slug}.html", "monthly", "0.9") for slug in slugs(published_only=True)]
    for path, freq, priority in SITEMAP_PAGES + landing_pages:
        loc = base + (home_path() if path == "HOME" else path)
        items.append(
            f"  <url><loc>{escape(loc)}</loc><changefreq>{freq}</changefreq>"
            f"<priority>{priority}</priority></url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(items)
        + "\n</urlset>\n"
    )
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")
