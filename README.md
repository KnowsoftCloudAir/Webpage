# Knowsoft Consult LTD — Corporate Website

Attractive multi-page site for **Knowsoft Consult LTD**: home (YouTube advert), software downloads, standard templates, about, and contact.

## Deploy on Render

1. Push this folder to GitHub.
2. New **Web Service** → connect repo.
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn app:app`
5. Environment (optional):
   - `YOUTUBE_VIDEO_ID` = your YouTube video id only (e.g. `abc123XYZ`)
   - `SECRET_KEY` = random string

## Local

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Customise

| Item | Where |
|------|--------|
| YouTube advert | Env `YOUTUBE_VIDEO_ID` or default in `app.py` |
| Software list | `SOFTWARE` in `app.py` |
| Templates list | `TEMPLATES_CATALOG` in `app.py` |
| Download files | `static/downloads/` |
| Logo | `static/img/knowsoft_logo.png` |
| Contact email shown | `templates/base.html` / `contact.html` |

Contact form appends leads to `instance/contact_leads.txt` (add SMTP later if needed).
