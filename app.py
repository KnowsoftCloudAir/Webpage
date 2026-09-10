"""
Knowsoft Consult LTD — Corporate website
Deploy on Render; assets can also be served from GitHub Pages mirror.
"""
import os
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "knowsoft-consult-change-me")

# YouTube promo (replace with your official advert video ID)
YOUTUBE_VIDEO_ID = os.environ.get("YOUTUBE_VIDEO_ID", "dQw4w9WgXcQ")  # placeholder — set env on Render

SOFTWARE = [
    {
        "id": "pfm-workflow",
        "name": "Project Financial Management Workflow",
        "tagline": "Inventory, expenses, budget variance & cost analytics",
        "version": "1.0",
        "platform": "Web + Windows installer",
        "icon": "bi-graph-up-arrow",
        "url": "https://contractconnect-inventory-mgt-5-0pv6.onrender.com/",
        "download": "/downloads/PFM_InnoSetup_Package.zip",
        "badge": "Flagship",
    },
    {
        "id": "churchgate",
        "name": "Churchgate",
        "tagline": "Church hierarchy, membership & growth analytics",
        "version": "1.0",
        "platform": "Web + Windows",
        "icon": "bi-building",
        "url": "#",
        "download": "#",
        "badge": "Enterprise",
    },
    {
        "id": "eprocurement",
        "name": "Knowsoft eProcurement",
        "tagline": "Vendor registration, quotations & LPO workflow",
        "version": "1.0",
        "platform": "Web",
        "icon": "bi-cart-check",
        "url": "#",
        "download": "#",
        "badge": "Business",
    },
]

TEMPLATES_CATALOG = [
    {"name": "Project Budget Template", "format": "Excel (.xlsx)", "category": "Finance", "file": "sample_budget_template.txt"},
    {"name": "Expense Claim Form", "format": "Word / PDF", "category": "Finance", "file": "sample_expense_form.txt"},
    {"name": "Variance Analysis Report", "format": "Excel (.xlsx)", "category": "Finance", "file": "sample_variance.txt"},
    {"name": "Consulting Proposal Outline", "format": "Word (.docx)", "category": "Consulting", "file": "sample_proposal.txt"},
    {"name": "Project Charter", "format": "Word (.docx)", "category": "PMO", "file": "sample_charter.txt"},
    {"name": "Risk Register", "format": "Excel (.xlsx)", "category": "PMO", "file": "sample_risk.txt"},
]

@app.context_processor
def inject_globals():
    return {
        "year": datetime.utcnow().year,
        "company": "Knowsoft Consult LTD",
        "youtube_id": YOUTUBE_VIDEO_ID,
    }

@app.route("/")
def home():
    return render_template("index.html", software=SOFTWARE[:3])

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/software")
def software():
    return render_template("software.html", items=SOFTWARE)

@app.route("/templates")
def templates_page():
    return render_template("templates_page.html", items=TEMPLATES_CATALOG)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        org = request.form.get("organization", "").strip()
        service = request.form.get("service", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Please complete name, email and message.", "warning")
            return redirect(url_for("contact"))
        # Store locally for Render demo (wire SMTP in production)
        log_dir = os.path.join(app.root_path, "instance")
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, "contact_leads.txt"), "a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.utcnow().isoformat()}Z ---\n")
            f.write(f"Name: {name}\nEmail: {email}\nOrg: {org}\nService: {service}\n{message}\n")
        flash("Thank you. Knowsoft Consult LTD will respond shortly.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")

@app.route("/downloads/<path:filename>")
def download_file(filename):
    folder = os.path.join(app.root_path, "static", "downloads")
    return send_from_directory(folder, filename, as_attachment=True)

@app.route("/health")
def health():
    return {"status": "ok", "site": "Knowsoft Consult LTD"}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
