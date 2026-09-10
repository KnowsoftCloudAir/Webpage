# Knowsoft Consult LTD Website

## Edit content (admin)
1. Open the site footer and click **…with ease** (small text, bottom right).
2. Password default: `Knowsoft@Admin2026` (change after first login; or set env `ADMIN_PASSWORD` before first run).
3. Update hero text, YouTube link, products (with video links), clients, password.
4. Upload gallery images from the same panel.

## Deploy (Render)
- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app`
- Env: `SECRET_KEY`, optional `ADMIN_PASSWORD`, optional `YOUTUBE_VIDEO_ID`

## Contact
- Lagos, Nigeria
- Knowsoftconsult@gmail.com
- +2348081650914
