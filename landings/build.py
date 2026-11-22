"""Збирає посадкові сторінки з даних у new-site/.

    .venv/bin/python -m landings.build

Оболонку (шапку й підвал) бере зі сторінки практики, щоб вони не розходилися.
"""

import json
import re
from html import escape
from pathlib import Path

from . import pages

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "new-site"
SHELL = SITE / "practice-viiskove.html"


def form(prefix, practice, button, note=True):
    extra = (
        '<p class="form-note">Передзвонимо в робочий час. Надсилаючи форму, ви погоджуєтеся з '
        '<a href="privacy.html">політикою конфіденційності</a>.</p>'
        if note else ""
    )
    name = (
        f'<div class="field"><label for="{prefix}-name">Ваше імʼя</label>'
        f'<input id="{prefix}-name" name="name" autocomplete="name"></div>'
        if prefix == "cta" else ""
    )
    return (
        f'<form class="{prefix}-form" data-lead-form data-practice="{practice}">{name}'
        f'<div class="field"><label for="{prefix}-contact">Телефон або Telegram</label>'
        f'<input id="{prefix}-contact" name="contact" autocomplete="tel" inputmode="tel" required></div>'
        f'<div class="field field-trap" aria-hidden="true"><label for="{prefix}-website">Сайт</label>'
        f'<input id="{prefix}-website" name="website" tabindex="-1" autocomplete="off"></div>'
        f'<button class="button" type="submit">{button} ↗</button>{extra}'
        '<p class="form-status" data-form-status role="status" aria-live="polite"></p></form>'
    )


def section(block):
    out = [f'<h2>{block["h"]}</h2>']
    out += [f"<p>{text}</p>" for text in block.get("p", [])]
    if block.get("ul"):
        out.append("<ul>" + "".join(f"<li>{item}</li>" for item in block["ul"]) + "</ul>")
    out += [f"<p>{text}</p>" for text in block.get("after", [])]
    return "\n    ".join(out)


def render(page):
    shell = SHELL.read_text(encoding="utf-8")
    head_end = shell.index("</head>")
    main_start = shell.index("<main>")
    main_end = shell.index("</main>") + len("</main>")
    head = shell[:head_end]
    head = re.sub(r"<title>.*?</title>", f"<title>{escape(page['title'])}</title>", head, count=1, flags=re.S)
    head = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{escape(page["description"])}">',
        head, count=1,
    )
    draft = not page.get("published")
    if draft:
        head += '<meta name="robots" content="noindex,nofollow">'
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in page["faq"]
        ],
    }
    head += f'<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>'

    card = page["card"]
    case = page.get("case")
    faq = "\n      ".join(
        f'<div class="faq-item"><button class="faq-q" type="button">{q}<span class="sign"></span></button>'
        f'<div class="faq-a"><p>{a}</p></div></div>'
        for q, a in page["faq"]
    )
    related = "".join(
        f'<a href="{href}">{label}<span class="ar">↗</span></a>' for label, href in page.get("related", [])
    )
    banner = (
        '<div class="draft-banner">Чернетка. Текст на перевірці адвоката, сторінку не опубліковано.</div>'
        if draft else ""
    )
    case_html = (
        '<h2>Кейс із нашої практики</h2>\n    <div class="case-list landing-case">'
        f'<a class="case" href="{case["href"]}"><div class="tag">{case["tag"]}</div><div>'
        f'<h2>«{case["title"]}»</h2><p>{case["text"]}</p></div><div class="go ar">↗</div></a></div>'
        if case else ""
    )
    main = f'''<main>{banner}
<section class="page-hero landing-hero"><div class="wrap"><div class="crumbs"><a href="aleshin-corporate.html">Головна</a> / <a href="practices.html">Практики</a> / {page["crumb"]}</div><span class="eyebrow">{page["eyebrow"]}</span><h1>{page["h1"]}</h1><p>{page["intro"]}</p>{form("hero", page["practice"], "Отримати консультацію", note=False)}</div></section>

<section class="section"><div class="wrap"><div class="svc-layout">
  <aside class="lawyer-card reveal-item">
    <div class="photo">{card["photo"]}</div>
    <div class="lc-body">
      <div class="lc-role">{card["role"]}</div>
      <h3>{card["name"]}</h3>
      <p class="lc-bio">{card["bio"]}</p>
      <div class="lc-contacts">
        <div><small>Email</small><a href="mailto:aleshin.partners@ukr.net">aleshin.partners@ukr.net</a></div>
        <div><small>Телефон</small><a href="tel:+380994000303">+38 (099) 400 03 03</a></div>
      </div>
      <a class="button" href="#zapyt">Залишити запит ↗</a>
    </div>
  </aside>

  <article class="svc-article">
    <p class="lead">{page["lead"]}</p>

    {(chr(10) + chr(10) + "    ").join(section(block) for block in page["sections"])}

    {case_html}

    <h2>Поширені запитання</h2>
    <div class="faq-accordion">
      {faq}
    </div>

    <h2>Повʼязані сторінки</h2>
    <div class="subservices">{related}</div>
  </article>
</div></div></section>

<div class="wrap" id="zapyt"><section class="cta"><h2>{page["cta"]["h"]}</h2><p>{page["cta"]["p"]}</p>{form("cta", page["practice"], "Надіслати запит")}</section></div></main>'''
    return head + shell[head_end:main_start] + main + shell[main_end:]


def main():
    for page in pages():
        target = SITE / f'{page["slug"]}.html'
        target.write_text(render(page), encoding="utf-8")
        state = "опубліковано" if page.get("published") else "чернетка"
        print(f"{target.relative_to(ROOT)} — {state}")


if __name__ == "__main__":
    main()
