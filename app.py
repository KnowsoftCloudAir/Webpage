"""
Knowsoft Consult LTD — Corporate website
"""
import json
import os
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, request, flash, redirect, url_for,
    send_from_directory, session, abort
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "knowsoft-consult-change-me-in-production")
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024
UPLOAD_DIR = os.path.join(app.root_path, "static", "uploads")
DATA_DIR = os.path.join(app.root_path, "instance")
CONTENT_FILE = os.path.join(DATA_DIR, "site_content.json")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

DEFAULT_CONTENT = {
    "youtube_id": os.environ.get("YOUTUBE_VIDEO_ID", ""),
    "hero_title": "Technology & consulting that work with ease",
    "hero_subtitle": "We design and deliver software platforms, financial workflows and advisory services for organisations that need clarity, control and results.",
    "address": "Lagos, Nigeria",
    "email": "Knowsoftconsult@gmail.com",
    "phone": "+2348081650914",
    "software": [
        {
            "id": "pfm-workflow",
            "name": "Project Financial Management Workflow",
            "tagline": "Inventory, expenses, budget variance and cost analytics",
            "version": "1.0",
            "platform": "Web + Windows",
            "icon": "bi-graph-up-arrow",
            "url": "https://contractconnect-inventory-mgt-5-0pv6.onrender.com/",
            "download": "",
            "video_url": "",
            "badge": "Flagship",
        },
        {
            "id": "churchgate",
            "name": "Churchgate",
            "tagline": "Church hierarchy, membership and growth analytics",
            "version": "1.0",
            "platform": "Web + Windows",
            "icon": "bi-building",
            "url": "",
            "download": "",
            "video_url": "",
            "badge": "Enterprise",
        },
        {
            "id": "eprocurement",
            "name": "Knowsoft eProcurement",
            "tagline": "Vendor registration, quotations and purchase workflow",
            "version": "1.0",
            "platform": "Web",
            "icon": "bi-cart-check",
            "url": "",
            "download": "",
            "video_url": "",
            "badge": "Business",
        },
    ],
    "templates": [
        {"name": "Project Budget Template", "format": "Excel", "category": "Finance", "file": "sample_budget_template.txt"},
        {"name": "Expense Claim Form", "format": "Word / PDF", "category": "Finance", "file": "sample_expense_form.txt"},
        {"name": "Variance Analysis Report", "format": "Excel", "category": "Finance", "file": "sample_variance.txt"},
        {"name": "Consulting Proposal Outline", "format": "Word", "category": "Consulting", "file": "sample_proposal.txt"},
        {"name": "Project Charter", "format": "Word", "category": "PMO", "file": "sample_charter.txt"},
        {"name": "Risk Register", "format": "Excel", "category": "PMO", "file": "sample_risk.txt"},
    ],
    "clients": [
        {"name": "Public sector partners", "sector": "Government"},
        {"name": "Development programmes", "sector": "Development"},
        {"name": "Faith & community organisations", "sector": "Non-profit"},
        {"name": "Private enterprises", "sector": "Private"},
    ],
    "gallery": [],
    "admin_password_hash": generate_password_hash(os.environ.get("ADMIN_PASSWORD", "Knowsoft@Admin2026")),
}

SERVICES = [
    {"slug": "capacity-building-financial-management", "title": "Capacity building in financial management", "icon": "bi-mortarboard", "summary": "Practical training that strengthens budgeting, controls and day-to-day financial discipline.", "body": "We design and deliver capacity-building programmes for finance teams, project units and leadership. Modules cover planning, documentation, internal controls and reporting discipline tailored to your operating environment."},
    {"slug": "office-management", "title": "Office management", "icon": "bi-briefcase", "summary": "Systems and routines for efficient, accountable office operations.", "body": "From filing and workflow design to supervision tools and service standards, we help offices run with clarity, measurable performance and reduced operational friction."},
    {"slug": "spot-check", "title": "Spot check", "icon": "bi-search", "summary": "Targeted reviews to verify compliance and safeguard resources.", "body": "Our spot-check assignments test whether policies and procedures are applied in practice. Findings are documented with practical recommendations and follow-up actions."},
    {"slug": "internal-audit", "title": "Internal audit", "icon": "bi-shield-check", "summary": "Independent assurance on controls, risk and process integrity.", "body": "We support internal audit planning, fieldwork and reporting aligned with professional standards—strengthening assurance without disrupting operations."},
    {"slug": "financial-accounting", "title": "Financial accounting", "icon": "bi-journal-text", "summary": "Accurate books, clean ledgers and reliable period closes.", "body": "Advisory and hands-on support for chart of accounts design, transaction processing discipline, reconciliations and period-end quality."},
    {"slug": "reporting", "title": "Reporting", "icon": "bi-file-earmark-bar-graph", "summary": "Clear management and donor-ready reports.", "body": "We help teams produce timely, decision-useful reports—management packs, donor formats and board summaries that match your stakeholder requirements."},
    {"slug": "software-installation-training", "title": "Software installation and training", "icon": "bi-pc-display", "summary": "Deploy tools correctly and train users to adopt them.", "body": "Installation, configuration, user training and go-live support for Knowsoft products and complementary financial systems."},
    {"slug": "baseline-assessment", "title": "Baseline assessment", "icon": "bi-clipboard-data", "summary": "Evidence-based starting point for reform and investment.", "body": "Structured assessments of systems, capacity and control environment to inform project design, financing decisions and improvement roadmaps."},
    {"slug": "financial-reporting", "title": "Financial reporting", "icon": "bi-graph-up", "summary": "High-quality statutory and management financial reporting.", "body": "Support for preparation, review and improvement of financial statements and management reporting frameworks."},
    {"slug": "financial-tools-erp-hardware", "title": "Supply of financial tools, ERPs and hardware", "icon": "bi-hdd-stack", "summary": "Software, ERPs and office hardware that match your needs.", "body": "We advise on and supply appropriate financial tools including ERP options, computers, printers and office shelving—aligned to budget and operational reality."},
    {"slug": "sop-development", "title": "SoP development", "icon": "bi-list-check", "summary": "Clear standard operating procedures your teams can follow.", "body": "Co-created SOPs for finance, admin and programme operations—practical, role-based and ready for training and compliance checks."},
    {"slug": "budget-preparation-guidance", "title": "Budget preparation and guidance", "icon": "bi-calculator", "summary": "Credible budgets with assumptions you can defend.", "body": "Facilitation and technical guidance for annual and project budgets, cost structures, assumptions and variance-ready monitoring frameworks."},
    {"slug": "cost-benefit-analysis", "title": "Cost benefit analysis", "icon": "bi-balance-scale", "summary": "Structured appraisal of options and investments.", "body": "We help decision-makers compare alternatives with transparent costs, benefits, risks and sensitivity analysis."},
    {"slug": "ifrs-training", "title": "IFRS training", "icon": "bi-book", "summary": "Practical IFRS capacity for finance professionals.", "body": "Training programmes on IFRS concepts and application, tailored to your sector and the standards most relevant to your reporting."},
]


def load_content():
    if not os.path.isfile(CONTENT_FILE):
        save_content(DEFAULT_CONTENT)
        return json.loads(json.dumps(DEFAULT_CONTENT))
    try:
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # fill missing keys
        for k, v in DEFAULT_CONTENT.items():
            if k not in data:
                data[k] = v
        return data
    except Exception:
        return json.loads(json.dumps(DEFAULT_CONTENT))


def save_content(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def admin_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get("ks_admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return wrapped


def youtube_embed_id(url_or_id):
    if not url_or_id:
        return ""
    s = url_or_id.strip()
    if "youtube.com" in s or "youtu.be" in s:
        if "v=" in s:
            return s.split("v=")[-1].split("&")[0]
        if "youtu.be/" in s:
            return s.split("youtu.be/")[-1].split("?")[0]
        if "embed/" in s:
            return s.split("embed/")[-1].split("?")[0]
    return s


@app.context_processor
def inject_globals():
    c = load_content()
    return {
        "year": datetime.utcnow().year,
        "company": "Knowsoft Consult LTD",
        "content": c,
        "services": SERVICES,
        "youtube_id": youtube_embed_id(c.get("youtube_id", "")),
    }


@app.route("/")
def home():
    c = load_content()
    return render_template("index.html", software=c.get("software", [])[:3])


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/software")
def software():
    c = load_content()
    return render_template("software.html", items=c.get("software", []))


@app.route("/templates")
def templates_page():
    c = load_content()
    return render_template("templates_page.html", items=c.get("templates", []))


@app.route("/services")
def services_index():
    return render_template("services.html")


@app.route("/services/<slug>")
def service_detail(slug):
    svc = next((s for s in SERVICES if s["slug"] == slug), None)
    if not svc:
        abort(404)
    return render_template("service_detail.html", svc=svc)


@app.route("/gallery")
def gallery():
    c = load_content()
    return render_template("gallery.html", images=c.get("gallery", []))


@app.route("/clients")
def clients():
    c = load_content()
    return render_template("clients.html", clients=c.get("clients", []))


@app.route("/request-consulting", methods=["GET", "POST"])
def request_consulting():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        org = request.form.get("organization", "").strip()
        service = request.form.get("service", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Please complete the required fields.", "warning")
            return redirect(url_for("request_consulting"))
        with open(os.path.join(DATA_DIR, "consulting_requests.txt"), "a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.utcnow().isoformat()}Z ---\n")
            f.write(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nOrg: {org}\nService: {service}\n{message}\n")
        flash("Thank you. Knowsoft Consult LTD has received your request.", "success")
        return redirect(url_for("request_consulting"))
    return render_template("request_consulting.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Please complete name, email and message.", "warning")
            return redirect(url_for("contact"))
        with open(os.path.join(DATA_DIR, "contact_leads.txt"), "a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.utcnow().isoformat()}Z ---\n")
            f.write(f"Name: {name}\nEmail: {email}\n{message}\n")
        flash("Thank you. We will respond shortly.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")


@app.route("/downloads/<path:filename>")
def download_file(filename):
    folder = os.path.join(app.root_path, "static", "downloads")
    return send_from_directory(folder, filename, as_attachment=True)


# Hidden admin entry — linked only from footer "…with ease"
@app.route("/ks-portal/sign-in", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password", "")
        c = load_content()
        if check_password_hash(c.get("admin_password_hash", ""), password):
            session["ks_admin"] = True
            flash("Welcome back.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("admin_login.html")


@app.route("/ks-portal/sign-out")
def admin_logout():
    session.pop("ks_admin", None)
    return redirect(url_for("home"))


@app.route("/ks-portal")
@admin_required
def admin_dashboard():
    c = load_content()
    return render_template("admin_dashboard.html", c=c)


@app.route("/ks-portal/save", methods=["POST"])
@admin_required
def admin_save():
    c = load_content()
    c["youtube_id"] = request.form.get("youtube_id", "").strip()
    c["hero_title"] = request.form.get("hero_title", c.get("hero_title", "")).strip()
    c["hero_subtitle"] = request.form.get("hero_subtitle", c.get("hero_subtitle", "")).strip()
    c["address"] = request.form.get("address", "Lagos, Nigeria").strip()
    c["email"] = request.form.get("email", "Knowsoftconsult@gmail.com").strip()
    c["phone"] = request.form.get("phone", "+2348081650914").strip()

    # Software rows
    names = request.form.getlist("sw_name")
    software = []
    for i, name in enumerate(names):
        if not name.strip():
            continue
        software.append({
            "id": request.form.getlist("sw_id")[i] if i < len(request.form.getlist("sw_id")) else f"item-{i}",
            "name": name.strip(),
            "tagline": request.form.getlist("sw_tagline")[i] if i < len(request.form.getlist("sw_tagline")) else "",
            "version": request.form.getlist("sw_version")[i] if i < len(request.form.getlist("sw_version")) else "1.0",
            "platform": request.form.getlist("sw_platform")[i] if i < len(request.form.getlist("sw_platform")) else "Web",
            "icon": request.form.getlist("sw_icon")[i] if i < len(request.form.getlist("sw_icon")) else "bi-app",
            "url": request.form.getlist("sw_url")[i] if i < len(request.form.getlist("sw_url")) else "",
            "download": request.form.getlist("sw_download")[i] if i < len(request.form.getlist("sw_download")) else "",
            "video_url": request.form.getlist("sw_video")[i] if i < len(request.form.getlist("sw_video")) else "",
            "badge": request.form.getlist("sw_badge")[i] if i < len(request.form.getlist("sw_badge")) else "",
        })
    if software:
        c["software"] = software

    # Clients
    client_names = request.form.getlist("client_name")
    clients = []
    for i, n in enumerate(client_names):
        if n.strip():
            sector = request.form.getlist("client_sector")[i] if i < len(request.form.getlist("client_sector")) else ""
            clients.append({"name": n.strip(), "sector": sector.strip()})
    if clients:
        c["clients"] = clients

    new_pw = request.form.get("new_password", "").strip()
    if new_pw and len(new_pw) >= 8:
        c["admin_password_hash"] = generate_password_hash(new_pw)

    save_content(c)
    flash("Site content saved.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/ks-portal/gallery", methods=["POST"])
@admin_required
def admin_gallery_upload():
    c = load_content()
    f = request.files.get("image")
    caption = request.form.get("caption", "").strip()
    if f and f.filename:
        name = secure_filename(f.filename)
        stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        fname = f"{stamp}_{name}"
        f.save(os.path.join(UPLOAD_DIR, fname))
        gallery = c.get("gallery", [])
        gallery.insert(0, {"file": fname, "caption": caption})
        c["gallery"] = gallery[:48]
        save_content(c)
        flash("Image added to gallery.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
