# Деплой на cPanel (Phusion Passenger)

Сайт «Альошин та Партнери» зібраний як Django-проєкт. Бази даних немає —
сторінки віддаються як шаблони, картинки з `assets/` через WhiteNoise.

## Структура

```
passenger_wsgi.py      ← точка входу для cPanel
manage.py
requirements.txt
.env.example           ← зразок змінних оточення
config/                ← settings.py / urls.py / wsgi.py
templates/             ← aleshin-luxe.html, privacy.html, robots.txt, sitemap.xml
assets/                ← джерело картинок
staticfiles/           ← сюди collectstatic складе статику (генерується)
```

## Локальний запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py runserver
# http://127.0.0.1:8000/
```

## Розгортання на cPanel

1. **Залий файли.** Завантаж проєкт у домашню теку додатку (напр. `~/aleshin`).
   Можна через Git, File Manager або FTP. Теку `.venv/` та `staticfiles/`
   заливати не треба — вони створяться на сервері.

2. **cPanel → Setup Python App → Create Application**
   - Python version: 3.8+ (бажано 3.10–3.11).
   - Application root: тека, куди залив проєкт (де лежить `passenger_wsgi.py`).
   - Application URL: твій домен.
   - Application startup file: `passenger_wsgi.py`.
   - Application Entry point: `application`.

3. **Environment variables** (там же, у налаштуваннях додатку):
   ```
   DJANGO_SECRET_KEY = <свій унікальний ключ>
   DJANGO_DEBUG      = false
   DJANGO_ALLOWED_HOSTS = aleshin.com.ua,www.aleshin.com.ua
   ```
   Згенерувати ключ:
   `python -c "import secrets; print(secrets.token_urlsafe(50))"`

4. **Встанови залежності.** У блоці додатку натисни «Run Pip Install»
   (вкаже на `requirements.txt`), або в терміналі cPanel активуй venv і:
   ```bash
   pip install -r requirements.txt
   ```

5. **Збери статику** (у терміналі cPanel, з активованим venv додатку):
   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Restart** додатку (кнопка Restart у Setup Python App).

Готово — сайт відкриється на твоєму домені.

## Що оновити перед публікацією

У файлах нижче поки прописаний старий GitHub Pages домен
`vonnabi.github.io/aleshin-partners-website` — заміни на свій:

- `templates/aleshin-luxe.html` — `<link rel="canonical">`, `og:url`, `og:image`
- `templates/privacy.html` — `<link rel="canonical">`
- `templates/sitemap.xml` — `<loc>`
- `templates/robots.txt` — `Sitemap:`

## Примітки

- Кожне редагування шаблонів/картинок на сервері → знову `collectstatic`
  (для картинок) і Restart додатку.
- `assets/legal-architecture.png` і `assets/asset-urls.txt` у `.gitignore` —
  якщо деплоїш через Git, переконайся, що потрібні картинки залиті.
