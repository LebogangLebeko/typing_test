import os
import sqlite3
import json
import html
import random
from flask import Flask, render_template, request, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Math Question Bank tailored per portfolio
MATH_QUESTIONS = {
    'Standard Bank': [
        {
            "id": 1,
            "question": "Mr. Leeu owes Imbuyiso's client R52,071.48 for services rendered. The client agreed to a settlement discount of 35%. What is the discounted settlement amount?",
            "options": ["R33,846.46", "R18,225.02", "R39,092.66", "R31,500.00"],
            "answer": "R33,846.46"
        },
        {
            "id": 2,
            "question": "Using the discounted settlement amount, calculate the installment value if he repays over 3 months by paying fortnightly (6 installments).",
            "options": ["R5,641.08", "R11,282.15", "R5,859.67", "R8,461.62"],
            "answer": "R5,641.08"
        },
        {
            "id": 3,
            "question": "What is the commission earned by the company on each fortnightly payment if we charge 15% commission (VAT included)?",
            "options": ["R846.16", "R1,692.32", "R735.79", "R1,025.00"],
            "answer": "R846.16"
        }
    ],
    'MFC': [
        {
            "id": 1,
            "question": "Mr. Leeu owes Imbuyiso's client R52,071.48 for services rendered. The client agreed to a settlement discount of 35%. What is the discounted settlement amount?",
            "options": ["R33,846.46", "R18,225.02", "R39,092.66", "R31,500.00"],
            "answer": "R33,846.46"
        },
        {
            "id": 2,
            "question": "Using the discounted settlement amount, calculate the installment value if he repays over 3 months by paying fortnightly (6 installments).",
            "options": ["R5,641.08", "R11,282.15", "R5,859.67", "R8,461.62"],
            "answer": "R5,641.08"
        },
        {
            "id": 3,
            "question": "What is the commission earned by the company on each fortnightly payment of R5,641.08 if we charge 15% commission (VAT included)?",
            "options": ["R846.16", "R1,692.32", "R735.79", "R1,025.00"],
            "answer": "R846.16"
        }
    ],
    'ABSA': [
        {
            "id": 1,
            "question": "An ABSA account holder owes an outstanding balance of R18,500.00. ABSA approves a 20% settlement discount if paid in full today. What is the required settlement payment?",
            "options": ["R14,800.00", "R14,200.00", "R3,700.00", "R15,100.00"],
            "answer": "R14,800.00"
        },
        {
            "id": 2,
            "question": "A monthly debit order of R2,200.00 fails twice. Each failure attracts a bank rejection fee of R115.00 and a tracking fee of R25.00. What is the total updated amount due including penalty fees?",
            "options": ["R2,480.00", "R2,340.00", "R2,280.00", "R2,620.00"],
            "answer": "R2,480.00"
        },
        {
            "id": 3,
            "question": "A debtor agrees to settle an ABSA balance of R9,600.00 via equal bi-weekly debit orders over 2 months (4 payments total). What is the value of each debit order?",
            "options": ["R2,400.00", "R4,800.00", "R1,200.00", "R3,200.00"],
            "answer": "R2,400.00"
        }
    ],
    'King Price': [
        {
            "id": 1,
            "question": "A King Price insured client lodges a motor claim of R45,000.00. The policy requires a standard excess of R3,500.00 plus an additional 5% excess on total claim value for young drivers. What is total excess amount payable?",
            "options": ["R5,750.00", "R2,250.00", "R3,500.00", "R5,250.00"],
            "answer": "R5,750.00"
        },
        {
            "id": 2,
            "question": "A client paid an annual insurance premium of R14,400.00 upfront and cancelled after 4 months. After deducting a 10% processing fee on the unearned 8-month balance, what refund is due to the client?",
            "options": ["R8,640.00", "R9,600.00", "R4,320.00", "R8,100.00"],
            "answer": "R8,640.00"
        },
        {
            "id": 3,
            "question": "An insurance policy lapsed after 3 consecutive missed monthly premiums of R1,250.00 each. To reinstate the policy, King Price requires payment of arrears plus a R150.00 reinstatement fee. What total payment is required?",
            "options": ["R3,900.00", "R3,750.00", "R4,100.00", "R3,850.00"],
            "answer": "R3,900.00"
        }
    ]
}

# POPI Question Bank with keyword matching engine
POPI_QUESTION_POOL = [
    {
        "id": 1,
        "title": "Purpose of the POPI Act",
        "question": "What is the primary purpose of the POPI Act when collecting, processing, or storing personal information?",
        "keywords": ["safeguard", "privacy", "responsible", "protect", "personal information", "rights", "processing", "collection", 
                     "storage", "sharing", "third party", "consent", "accuracy", "security", "confidentiality", "integrity", "transparency",
                     "accountability", "data subject", "information officer", "regulatory compliance", "legal obligations",
                     "breach notification", "penalties for non-compliance", "financial consequences", "imprisonment", "regulatory authority oversight",
                     "information management practices", "data handling procedures", "information security measures", "data privacy policies",
                     "information governance frameworks", "data retention policies", "data minimization principles", "data accuracy requirements",
                     "data integrity standards", "data confidentiality protocols", "data security safeguards", "data subject consent requirements",
                     "data processing agreements", "data sharing agreements", "data transfer protocols", "data breach response plans",
                     "data protection impact assessments", "data protection officer responsibilities", "data protection training programs",
                     "data protection audits", "data protection certifications", "data protection compliance monitoring", "data protection risk assessments",
                     "data protection incident response procedures", "data protection breach reporting obligations", "data protection regulatory reporting requirements",
                     "data protection enforcement actions"]
    },
    {
        "id": 2,
        "title": "Definition of Personal Information",
        "question": "List at least 4 items that fall under the definition of 'Personal Information' in debt collection.",
        "keywords": ["marital", "identity", "id number", "email", "address", "telephone", "phone", "cell", "financial", 
                     "bank", "account", "credit", "debit", "loan", "employment", "income", "medical", "health", "sensitive information",
                     "personal data", "contact details", "demographic information", "biometric data", "location data", "online identifiers",
                     "social media profiles", "government-issued identifiers", "tax information", "educational records",
                     "professional licenses", "criminal records", "legal documents", "family information", "next of kin details",
                     "emergency contact information", "personal preferences", "cultural background", "religious beliefs", "political affiliations",
                     "sexual orientation", "gender identity", "race or ethnicity", "nationality", "passport information", "driver's license information",
                     "vehicle registration information", "insurance policy information", "financial transaction history", "credit score",
                     "debt history", "payment history", "collection agency records", "court records", "legal proceedings information",
                     "employment history", "salary information", "benefits information", "healthcare records", "medical history",
                     "prescription information", "allergy information", "genetic information", "family medical history", "mental health records",
                     "substance abuse records", "disability information", "veteran status", "military service records", "immigration status",
                     "citizenship information", "residency status", "travel history", "visa information", "criminal background checks",
                     "fingerprint data", "facial recognition data", "voice recognition data", "retina scan data", "DNA samples",
                     "geolocation data", "IP address information", "device identifiers", "cookies and tracking technologies", "online activity logs",
                     "social media activity", "email communications", "text message records", "call logs", "video recordings",
                     "photographs", "audio recordings", "surveillance footage", "public records", "government databases", "third-party data sources",
                     "data brokers", "marketing databases", "consumer profiling information", "behavioral data", "psychographic data",
                     "purchase history", "transactional data", "loyalty program information", "membership information", "subscription details",
                     "preferences and interests", "opinions and feedback", "survey responses", "contest entries", "event registrations",
                     "online reviews", "user-generated content", "forum posts", "blog comments", "social networking interactions",
                     "chat logs", "instant messaging records", "video conferencing records", "collaboration platform data", "cloud storage data",
                     "file sharing records", "document metadata", "version history", "audit trails", "access logs", "security incident reports",
                     "data breach notifications", "regulatory compliance reports", "legal correspondence", "contractual agreements",
                     "terms of service agreements", "privacy policy acknowledgments", "consent forms", "waivers and releases", "non-disclosure agreements",
                     "intellectual property records", "patent filings", "trademark registrations", "copyright information", "licensing agreements",]
    },
    {
        "id": 3,
        "title": "Conditions for Lawful Processing",
        "question": "Under what conditions can personal information be lawfully processed, and what is required regarding accuracy?",
        "keywords": ["consent", "contract", "lawfully", "reasonably", "complete", "accurate", "updated", "correct", "relevant", "not excessive", 
                     "necessary", "purpose limitation", "data minimization", "storage limitation", "integrity", "confidentiality", "security", 
                     "accountability", "transparency", "data subject rights", "information officer responsibilities", "regulatory compliance",
                     "legal obligations", "breach notification", "penalties for non-compliance", "financial consequences", "imprisonment",
                     "regulatory authority oversight", "information management practices", "data handling procedures", 
                     "information security measures", "data privacy policies", "information governance frameworks",
                     "data retention policies", "data minimization principles", "data accuracy requirements",
                     "data integrity standards", "data confidentiality protocols", "data security safeguards",
                     "data subject consent requirements", "data processing agreements", "data sharing agreements",
                     "data transfer protocols", "data breach response plans", "data protection impact assessments",
                     "data protection officer responsibilities", "data protection training programs", "data protection audits",
                     "data protection certifications", "data protection compliance monitoring", "data protection risk assessments",
                     "data protection incident response procedures", "data protection breach reporting obligations",
                     "data protection regulatory reporting requirements", "data protection enforcement actions"]
    },
    {
        "id": 4,
        "title": "Notification Requirements",
        "question": "What information must you disclose to a debtor when collecting personal information during communication?",
        "keywords": ["aware", "collection", "disclose", "who we are", "imbuyiso", "client", "bank", "purpose", "arrears",
                     "settlement", "debt", "collection", "legal", "regulatory", "privacy", "personal information", "data protection",
                     "information security", "data privacy", "information governance", "data retention", "data minimization",
                     "data accuracy", "data integrity", "data confidentiality", "data security", "data subject rights",
                     "information officer responsibilities", "regulatory compliance", "legal obligations",
                     "breach notification", "penalties for non-compliance", "financial consequences", "imprisonment",
                     "regulatory authority oversight", "information management practices", "data handling procedures",
                     "information security measures", "data privacy policies", "information governance frameworks",
                     "data retention policies", "data minimization principles", "data accuracy requirements",
                     "data integrity standards", "data confidentiality protocols", "data security safeguards",
                     "data subject consent requirements", "data processing agreements", "data sharing agreements",
                     "data transfer protocols", "data breach response plans", "data protection impact assessments",
                     "data protection officer responsibilities", "data protection training programs", "data protection audits",
                     "data protection certifications", "data protection compliance monitoring", "data protection risk assessments",
                     "data protection incident response procedures", "data protection breach reporting obligations",
                     "data protection regulatory reporting requirements", "data protection enforcement actions"]
    },
    {
        "id": 5,
        "title": "Security Safeguards",
        "question": "What are your responsibilities regarding security safeguards and access to personal information?",
        "keywords": ["integrity", "confidentiality", "secure", "debtor alone", "no other person", "unauthorized", "encrypt", "data protection",
                     "information security", "data privacy", "information governance", "data retention", "data minimization",
                     "data accuracy", "data integrity", "data confidentiality", "data security", "data subject rights",
                     "information officer responsibilities", "regulatory compliance", "legal obligations",
                     "breach notification", "penalties for non-compliance", "financial consequences", "imprisonment",
                     "regulatory authority oversight", "information management practices", "data handling procedures",
                     "information security measures", "data privacy policies", "information governance frameworks",
                     "data retention policies", "data minimization principles", "data accuracy requirements",
                     "data integrity standards", "data confidentiality protocols", "data security safeguards",
                     "data subject consent requirements", "data processing agreements", "data sharing agreements",
                     "data transfer protocols", "data breach response plans", "data protection impact assessments",
                     "data protection officer responsibilities", "data protection training programs", "data protection audits",
                     "data protection certifications", "data protection compliance monitoring", "data protection risk assessments",
                     "data protection incident response procedures", "data protection breach reporting obligations",
                     "data protection regulatory reporting requirements", "data protection enforcement actions",
                     "access control", "user authentication", "role-based access", "least privilege", "audit logging", 
                     "monitoring", "incident response", "data encryption", "secure storage", "data masking", "data anonymization",
                     "data pseudonymization", "data classification", "data labeling", "data retention policies",
                     "data disposal procedures", "data backup and recovery", "network security", "firewall protection",
                     "intrusion detection", "intrusion prevention", "security awareness training", "security policies and procedures",
                     "security audits and assessments", "third-party vendor management", "data breach response plans",
                     "data breach notification procedures", "regulatory compliance monitoring", "legal obligations",
                     "breach notification", "penalties for non-compliance", "financial consequences", "imprisonment",
                     "regulatory authority oversight", "information management practices", "data handling procedures",
                     "information security measures", "data privacy policies", "information governance frameworks",
                     "data retention policies", "data minimization principles", "data accuracy requirements",
                     "data integrity standards", "data confidentiality protocols", "data security safeguards",
                     "data subject consent requirements", "data processing agreements", "data sharing agreements",
                     "data transfer protocols", "data breach response plans", "data protection impact assessments",
                     "data protection officer responsibilities", "data protection training programs", "data protection audits",
                     "data protection certifications", "data protection compliance monitoring", "data protection risk assessments"
                    ]
    },
    {
        "id": 6,
        "title": "Actions Constituting a Breach",
        "question": "Name 4 actions during calls or correspondence that would constitute a direct breach of the POPI Act.",
        "keywords": ["sms", "email", "unconfirmed", "third party", "recording", "script", "template", "identity", "disclose", "incorrect", "id number", "not confirming",
                     "account information", "personal information", "sensitive information", "confidentiality", "privacy", "data protection", 
                     "information security", "data privacy", "information governance", "data retention", "data minimization", "data accuracy", 
                     "data integrity", "data confidentiality", "data security", "data subject rights", "information officer responsibilities",
                     "regulatory compliance", "legal obligations", "breach notification", "penalties for non-compliance", "financial consequences", 
                     "imprisonment", "regulatory authority oversight", "information management practices", "data handling procedures", 
                     "information security measures", "data privacy policies", "information governance frameworks", "data retention policies", 
                     "data minimization principles", "data accuracy requirements", "data integrity standards", "data confidentiality protocols", 
                     "data security safeguards", "data subject consent requirements", "data processing agreements", "data sharing agreements", 
                     "data transfer protocols", "data breach response plans", "data protection impact assessments", 
                     "data protection officer responsibilities", "data protection training programs", "data protection audits", 
                     "data protection certifications", "data protection compliance monitoring", "data protection risk assessments", 
                     "data protection incident response procedures", "data protection breach reporting obligations", 
                     "data protection regulatory reporting requirements", "data protection enforcement actions"]
    },
    {
        "id": 7,
        "title": "Legal & Financial Consequences",
        "question": "What are the legal and financial consequences for Imbuyiso if the POPI Act is breached?",
        "keywords": ["10 million", "fine", "prosecution", "imprisonment", "12 months", "regulator", "closure", "stop"
                     , "operations", "legal action", "civil liability", "damages", "compensation", "reputational damage", "loss of business",
                     "loss of clients", "loss of trust", "loss of credibility", "regulatory sanctions", "regulatory penalties",
                     "regulatory enforcement actions", "regulatory investigations", "regulatory audits", "regulatory inspections", 
                     "regulatory compliance monitoring", "regulatory reporting requirements", "regulatory breach notifications", 
                     "regulatory enforcement proceedings", "regulatory legal actions", "regulatory financial penalties",
                     "regulatory reputational impact", "regulatory stakeholder communication", "regulatory public relations management",
                     "regulatory crisis management", "regulatory risk assessments", "regulatory incident response plans",
                     "regulatory incident investigation procedures", "regulatory incident mitigation strategies", 
                     "regulatory incident communication protocols", "regulatory incident documentation requirements", 
                     "regulatory incident follow-up actions", "regulatory incident lessons learned", "regulatory incident reporting obligations", 
                     "regulatory incident regulatory reporting requirements", "regulatory incident enforcement actions",
                     "regulatory incident legal obligations", "regulatory incident financial consequences",
                     "regulatory incident reputational impact", "regulatory incident stakeholder communication", 
                     "regulatory incident public relations management", "regulatory incident crisis management"]
    },
    {
        "id": 8,
        "title": "Verification Protocol",
        "question": "Why is strict identity verification required before discussing or corresponding about account details?",
        "keywords": ["correct person", "verify", "identity", "confidentiality", "third party", "debtor", "personal information", "sensitive information", "privacy", "data protection", "information security", 
                     "data privacy", "information governance", "data retention", "data minimization", "data accuracy", 
                     "data integrity", "data confidentiality", "data security", "data subject rights", 
                     "information officer responsibilities", "regulatory compliance", "legal obligations", 
                     "breach notification", "penalties for non-compliance", "financial consequences", 
                     "imprisonment", "regulatory authority oversight", "information management practices",
                     "data handling procedures", "information security measures", "data privacy policies",
                     "information governance frameworks", "data retention policies", "data minimization principles",
                     "data accuracy requirements", "data integrity standards", "data confidentiality protocols",
                     "data security safeguards", "data subject consent requirements", "data processing agreements", "data sharing agreements",
                     "data transfer protocols", "data breach response plans", "data protection impact assessments"]
    },
    {
        "id": 9,
        "title": "Internal Company Consequences",
        "question": "What internal disciplinary action can Imbuyiso take against an employee for non-adherence to the POPI Act?",
        "keywords": ["disciplinary", "dismissal", "termination", "non-adherence", "hearing", "warning", "suspension", "reprimand", "performance improvement plan", "training", "coaching", "counseling", "investigation", 
                     "policy violation", "code of conduct violation", "ethics violation", "compliance violation", "regulatory violation",
                     "legal violation", "contractual violation", "confidentiality breach", "privacy breach", "data protection breach",
                     "information security breach", "data privacy breach", "information governance breach", 
                     "data retention breach", "data minimization breach", "data accuracy breach", "data integrity breach", 
                     "data confidentiality breach", "data security breach", 
                     "data subject rights violation", "information officer responsibilities violation",
                     "regulatory compliance violation", "legal obligations violation", "breach notification violation",
                     "penalties for non-compliance violation", "financial consequences violation", "imprisonment violation",
                     "regulatory authority oversight violation", "information management practices violation",
                     "data handling procedures violation", "information security measures violation",
                     "data privacy policies violation", "information governance frameworks violation",
                     "data retention policies violation", "data minimization principles violation", "data accuracy requirements violation",
                     "data integrity standards violation", "data confidentiality protocols violation", "data security safeguards violation",
                     "data subject consent requirements violation", "data processing agreements violation", "data sharing agreements violation",
                     "data transfer protocols violation", "data breach response plans violation", "data protection impact assessments violation"]
    }
]

def evaluate_popi_answers(submitted_answers):
    if not submitted_answers:
        return 0.0
    total_score = 0
    for item in submitted_answers:
        q_id = int(item.get('id', 0))
        user_text = str(item.get('answer', '')).lower()
        
        q_config = next((q for q in POPI_QUESTION_POOL if q['id'] == q_id), None)
        if not q_config:
            continue
            
        matched = [kw for kw in q_config['keywords'] if kw.lower() in user_text]
        # Require 2 matched keywords for passing credit, 3+ for 100%
        if len(matched) >= 3:
            q_score = 100
        elif len(matched) == 2:
            q_score = 75
        elif len(matched) == 1:
            q_score = 50
        else:
            q_score = 0
        total_score += q_score
        
    return round(total_score / len(submitted_answers), 2)

def get_grade(score, threshold=70.0):
    return "PASS" if score >= threshold else "FAIL"

def init_db():
    conn = sqlite3.connect('typing.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
   
    columns = [
        ("selected_book", "TEXT"), ("audio_cps", "REAL"), ("audio_accuracy", "REAL"), ("part1_grade", "TEXT"),
        ("typing_gross_wpm", "REAL"), ("typing_net_wpm", "REAL"), ("typing_accuracy", "REAL"), ("part2_grade", "TEXT"),
        ("maths_score", "REAL"), ("popi_score", "REAL"),
        ("total_score", "REAL"), ("final_grade", "TEXT"),
        ("part1_data", "TEXT"), ("p2_typed", "TEXT"), ("p2_target", "TEXT"),
        ("math_data", "TEXT"), ("popi_data", "TEXT")
    ]
    for col_name, col_type in columns:
        try:
            c.execute(f"ALTER TABLE results ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()

init_db()

def calculate_wpm_metrics(target_text, typed_text, time_taken_seconds=60):
    target_words = str(target_text).split()
    typed_words = str(typed_text).split()
   
    correct_words = 0
    for i in range(min(len(target_words), len(typed_words))):
        if target_words[i] == typed_words[i]:
            correct_words += 1
           
    accuracy_percentage = (correct_words / len(target_words)) * 100 if target_words else 0
   
    minutes = time_taken_seconds / 60
    total_chars = len(typed_text)
   
    gross_wpm = (total_chars / 5) / minutes if minutes > 0 else 0
    errors = len(typed_words) - correct_words
    net_wpm = gross_wpm - (errors / minutes) if minutes > 0 else 0
   
    return round(accuracy_percentage, 2), round(gross_wpm), max(0, round(net_wpm))

def generate_part2_diff(typed_text, target_text):
    typed_words = str(typed_text or '').split()
    target_words = str(target_text or '').split()
    result = []
   
    for i, t_word in enumerate(target_words):
        t_word_esc = html.escape(t_word)
        if i < len(typed_words):
            typed_esc = html.escape(typed_words[i])
            if typed_words[i] == t_word:
                result.append(f'<font color="green"><b>{t_word_esc}</b></font>')
            else:
                result.append(f'<font color="red"><s>{typed_esc}</s></font> <font color="#888888"><b>{t_word_esc}</b></font>')
        else:
            result.append(f'<font color="#888888">{t_word_esc}</font>')
           
    return " ".join(result)

def generate_combined_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    styles = getSampleStyleSheet()
   
    custom_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13
    )

    def draw_letterhead():
        if os.path.exists("static/logo.png"):
            logo_width = 140
            center_x = (width - logo_width) / 2
            c.drawImage("static/logo.png", center_x, height - 80, width=logo_width, height=45, preserveAspectRatio=True, mask='auto')
       
        c.setFont("Helvetica-Bold", 8)
        c.drawRightString(560, height - 40, "BROOKLYN COURT, 361 VEALE STREET")
        c.drawRightString(560, height - 51, "NIEUW MUCKLENEUK, PRETORIA, 0181")
        c.setFont("Helvetica", 8)
        c.drawRightString(560, height - 62, "TEL: (012) 762 0300")
        c.drawRightString(560, height - 73, "INFO@IMBUYISO.CO.ZA | www.imbuyiso.co.za")
       
        c.setFillColor(colors.HexColor("#444444"))
        c.setFont("Helvetica", 7)
        c.drawString(50, height - 95, "IMBUYISO CONSULTING & COLLECTIONS (PTY) LTD | Reg No. 2006/028785/07")
       
        c.setStrokeColor(colors.HexColor("#D4A017"))
        c.setLineWidth(2)
        c.line(50, height - 102, 560, height - 102)
        c.setFillColor(colors.black)

    # ==========================================
    # PAGE 1: AUDIO & TYPING TRANSCRIPT ANALYSIS
    # ==========================================
    draw_letterhead()
   
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, height - 125, "CANDIDATE SKILLS ASSESSMENT REPORT (PAGE 1 OF 3)")
   
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    c.rect(50, height - 165, 510, 30, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(60, height - 150, f"Candidate: {data.get('username', 'Unknown')} | Portfolio: {data.get('selected_book', 'General')}")
    c.setFont("Helvetica", 9)
    c.drawString(60, height - 160, "Assessment Component: Raw Input & Accuracy Breakdown")

    y_pos = height - 185

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_pos, "Part 1: Audio Transcription Field Details")
    y_pos -= 12

    p1_data = data.get('part1_data', [])
    p1_html = ""
    for item in p1_data:
        t_words = str(item.get('typed') or '').split()
        tgt_words = str(item.get('target') or '').split()
       
        typed_html = []
        for i in range(max(len(t_words), len(tgt_words))):
            if i < len(t_words) and i < len(tgt_words):
                t_esc = html.escape(t_words[i])
                if t_words[i] == tgt_words[i]:
                    typed_html.append(f'<font color="green">{t_esc}</font>')
                else:
                    typed_html.append(f'<font color="red"><u>{t_esc}</u></font>')
            elif i < len(t_words):
                t_esc = html.escape(t_words[i])
                typed_html.append(f'<font color="red"><u>{t_esc}</u></font>')
               
        user_input_html = " ".join(typed_html) if t_words else "<font color='red'><i>[Left Blank]</i></font>"
        tgt_label_esc = html.escape(item.get('label', ''))
        tgt_full_esc = html.escape(item.get('target', ''))
       
        p1_html += f"<b>{tgt_label_esc}:</b> Expected: <font color='#888888'>{tgt_full_esc}</font> | Input: {user_input_html}<br/>"

    p1_paragraph = Paragraph(p1_html, custom_style)
    w, h = p1_paragraph.wrap(500, 800)
    y_pos -= h
    p1_paragraph.drawOn(c, 50, y_pos)
    y_pos -= 20

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_pos, "Part 2: 60-Second Copy Typing Transcript Analysis")
    y_pos -= 12
   
    p2_html = generate_part2_diff(data.get('p2_typed', ''), data.get('p2_target', ''))
    p2_paragraph = Paragraph(p2_html, custom_style)
    w, h = p2_paragraph.wrap(500, 800)
    y_pos -= h
    p2_paragraph.drawOn(c, 50, y_pos)

    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(50, 30, "* Continued on Page 2 for Mathematics and POPI Act breakdowns.")

    # ==========================================
    # PAGE 2: MATH & POPI ACT BREAKDOWN
    # ==========================================
    c.showPage()
    draw_letterhead()

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, height - 125, "CANDIDATE SKILLS ASSESSMENT REPORT (PAGE 2 OF 3)")

    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    c.rect(50, height - 165, 510, 30, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(60, height - 150, f"Candidate: {data.get('username', 'Unknown')} | Portfolio: {data.get('selected_book', 'General')}")
    c.setFont("Helvetica", 9)
    c.drawString(60, height - 160, "Assessment Component: Math & POPI Act Answer Breakdown")

    y_pos = height - 195

    # -------------------
    # MATH BREAKDOWN
    # -------------------
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_pos, f"Part 3: Portfolio Mathematics ({data.get('selected_book', 'Standard Bank')}) Details")
    y_pos -= 12

    selected_book = data.get('selected_book', 'Standard Bank')
    book_questions = MATH_QUESTIONS.get(selected_book, MATH_QUESTIONS['Standard Bank'])
    math_user_answers = data.get('math_answers', {})

    math_html = ""
    for q in book_questions:
        q_key = f"q_{q['id']}"
        user_ans = math_user_answers.get(q_key, "")
        expected_ans = q['answer']
        
        user_ans_esc = html.escape(str(user_ans)) if user_ans else "<i>[Left Blank]</i>"
        expected_ans_esc = html.escape(str(expected_ans))
        
        if str(user_ans).strip().lower() == str(expected_ans).strip().lower():
            input_fmt = f'<font color="green">{user_ans_esc}</font>'
        else:
            input_fmt = f'<font color="red"><u>{user_ans_esc}</u></font>'
            
        math_html += f"<b>Q: {html.escape(q['question'])}</b><br/>"
        math_html += f"Expected: <font color='#888888'>{expected_ans_esc}</font> | Input: {input_fmt}<br/><br/>"

    if math_html:
        math_p = Paragraph(math_html, custom_style)
        w, h = math_p.wrap(500, 800)
        math_p.drawOn(c, 50, y_pos - h)
        y_pos -= (h + 20)

    # -------------------
    # POPI BREAKDOWN
    # -------------------
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_pos, "Part 4: POPI Act Compliance Details")
    y_pos -= 12

    popi_user_answers = data.get('popi_answers', [])
    popi_html = ""
    for item in popi_user_answers:
        q_id = int(item.get('id', 0))
        user_text = item.get('answer', '')
        q_config = next((q for q in POPI_QUESTION_POOL if q['id'] == q_id), None)
        
        if q_config:
            expected_kws = ", ".join(q_config['keywords'])
            user_ans_esc = html.escape(str(user_text)) if user_text else "<i>[Left Blank]</i>"
            
            # Highlight answer input based on keyword matches
            matched = [kw for kw in q_config['keywords'] if kw.lower() in str(user_text).lower()]
            if len(matched) >= 3:
                color = "green" # Full marks
            elif len(matched) > 0:
                color = "#D4A017" # Orange for partial marks
            else:
                color = "red" # Failed match
                
            popi_html += f"<b>Q: {html.escape(q_config['question'])}</b><br/>"
            popi_html += f"Expected Keywords: <font color='#888888'>{html.escape(expected_kws)}</font><br/>"
            popi_html += f"Input: <font color='{color}'>{user_ans_esc}</font><br/><br/>"

    if popi_html:
        popi_p = Paragraph(popi_html, custom_style)
        w, h = popi_p.wrap(500, 800)
        popi_p.drawOn(c, 50, y_pos - h)
        y_pos -= (h + 20)

    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(50, 30, "* Continued on Page 3 for Final Score Calculations and Pass/Fail Outcome.")

    # ==========================================
    # PAGE 3: SCORE BREAKDOWN (Final Outcome)
    # ==========================================
    c.showPage()
    draw_letterhead()

    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.black)
    c.drawString(50, height - 125, "FINAL ASSESSMENT OUTCOME REPORT (PAGE 3 OF 3)")

    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    c.rect(50, height - 165, 510, 30, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(60, height - 150, f"Candidate: {data.get('username', 'Unknown')} | Portfolio: {data.get('selected_book', 'General')}")
    c.setFont("Helvetica", 9)
    c.drawString(60, height - 160, "Modules Calculated: Audio, Book Math, POPI Act & Copy Typing")

    y_p2 = height - 190

    # AUDIO RESULTS
    c.setFillColor(colors.HexColor("#F8F9FA"))
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.rect(50, y_p2 - 55, 510, 55, fill=1, stroke=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(65, y_p2 - 18, "PART 1: AUDIO TRANSCRIPTION")
    c.setFont("Helvetica", 9)
    c.drawString(65, y_p2 - 38, f"Calculated Score: {data.get('audio_accuracy', 0)}%")
    
    p1_grade = data.get('part1_grade', 'FAIL')
    c.setFont("Helvetica-Bold", 9)
    c.drawString(420, y_p2 - 38, "Status: ")
    c.setFillColor(colors.green if p1_grade == "PASS" else colors.red)
    c.drawString(465, y_p2 - 38, p1_grade)

    y_p2 -= 65

    # MATH RESULTS
    maths_score = data.get('maths_score', 0)
    c.setFillColor(colors.HexColor("#F8F9FA"))
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.rect(50, y_p2 - 55, 510, 55, fill=1, stroke=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(65, y_p2 - 18, f"PART 2: PORTFOLIO MATHEMATICS ({data.get('selected_book', 'Standard Bank')})")
    c.setFont("Helvetica", 9)
    c.drawString(65, y_p2 - 38, f"Calculated Score: {maths_score}%")
    m_grade = get_grade(float(maths_score))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(420, y_p2 - 38, "Status: ")
    c.setFillColor(colors.green if m_grade == "PASS" else colors.red)
    c.drawString(465, y_p2 - 38, m_grade)

    y_p2 -= 65

    # POPI RESULTS
    popi_score = data.get('popi_score', 0)
    c.setFillColor(colors.HexColor("#F8F9FA"))
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.rect(50, y_p2 - 55, 510, 55, fill=1, stroke=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(65, y_p2 - 18, "PART 3: POPI ACT COMPLIANCE")
    c.setFont("Helvetica", 9)
    c.drawString(65, y_p2 - 38, f"Calculated Score: {popi_score}%")
    popi_grade = get_grade(float(popi_score))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(420, y_p2 - 38, "Status: ")
    c.setFillColor(colors.green if popi_grade == "PASS" else colors.red)
    c.drawString(465, y_p2 - 38, popi_grade)

    y_p2 -= 65

    # TYPING RESULTS
    c.setFillColor(colors.HexColor("#F8F9FA"))
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.rect(50, y_p2 - 55, 510, 55, fill=1, stroke=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(65, y_p2 - 18, "PART 4: 60-SECOND COPY TYPING")
    c.setFont("Helvetica", 9)
    c.drawString(65, y_p2 - 38, f"Calculated Score: {data.get('typing_accuracy', 0)}%")
    
    p2_grade = data.get('part2_grade', 'FAIL')
    c.setFont("Helvetica-Bold", 9)
    c.drawString(420, y_p2 - 38, "Status: ")
    c.setFillColor(colors.green if p2_grade == "PASS" else colors.red)
    c.drawString(465, y_p2 - 38, p2_grade)

    y_p2 -= 80

    # OVERALL OUTCOME
    c.setStrokeColor(colors.HexColor("#1A365D"))
    c.setLineWidth(2)
    c.setFillColor(colors.HexColor("#EEF2F7"))
    c.rect(50, y_p2 - 90, 510, 90, fill=1, stroke=1)
   
    c.setFillColor(colors.HexColor("#1A365D"))
    c.setFont("Helvetica-Bold", 12)
    c.drawString(65, y_p2 - 25, "OVERALL ASSESSMENT COMBINED SCORE")
   
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(65, y_p2 - 50, f"FINAL PERCENTAGE MARK: {data.get('total_score', 0)}%")
   
    final_grade = data.get('final_grade', 'FAIL')
    c.drawString(65, y_p2 - 75, "FINAL OVERALL OUTCOME:")
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.green if final_grade == "PASS" else colors.red)
    c.drawString(240, y_p2 - 75, final_grade)

    c.save()

# Routes
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/audio_test')
def audio_test():
    return render_template('audio_test.html')

@app.route('/math_test')
def math_test():
    book = request.args.get('book', 'Standard Bank')
    questions = MATH_QUESTIONS.get(book, MATH_QUESTIONS['Standard Bank'])
    return render_template('maths_test.html', questions=questions, book=book)

@app.route('/popi_test')
def popi_test():
    selected_questions = random.sample(POPI_QUESTION_POOL, 3)
    return render_template('popi_test.html', questions=selected_questions)

@app.route('/typing_test')
def typing_test():
    return render_template('typing_test.html')

@app.route('/save_score', methods=['POST'])
def save_score():
    d = request.json
    selected_book = d.get('selected_book', 'Standard Bank')
   
    # Typing metrics
    p2_acc, p2_gross, p2_net = calculate_wpm_metrics(d.get('p2_target', ''), d.get('p2_typed', ''), 60)
    part1_grade = get_grade(float(d.get('audio_accuracy', 0)))
    part2_grade = get_grade(p2_acc)
   
    # Evaluate Math Answers against Answer Key
    math_user_answers = d.get('math_answers', {})
    book_questions = MATH_QUESTIONS.get(selected_book, MATH_QUESTIONS['Standard Bank'])
    correct_math_count = 0
    for q in book_questions:
        q_key = f"q_{q['id']}"
        if math_user_answers.get(q_key) == q['answer']:
            correct_math_count += 1
    maths_score = round((correct_math_count / len(book_questions)) * 100, 2)

    # Evaluate POPI Answers against Keywords
    popi_user_answers = d.get('popi_answers', [])
    popi_score = evaluate_popi_answers(popi_user_answers)
   
    # Calculate Overall Score (Average of 4 components)
    score_components = [
        float(d.get('audio_accuracy', 0)),
        p2_acc,
        maths_score,
        popi_score
    ]
    total_score = round(sum(score_components) / len(score_components), 2)
    final_grade = get_grade(total_score)
   
    d['selected_book'] = selected_book
    d['typing_accuracy'] = p2_acc
    d['typing_gross_wpm'] = p2_gross
    d['typing_net_wpm'] = p2_net
    d['part1_grade'] = part1_grade
    d['part2_grade'] = part2_grade
    d['maths_score'] = maths_score
    d['popi_score'] = popi_score
    d['total_score'] = total_score
    d['final_grade'] = final_grade

    conn = sqlite3.connect('typing.db')
    c = conn.cursor()
    c.execute('''INSERT INTO results
                 (username, selected_book, audio_cps, audio_accuracy, part1_grade, typing_gross_wpm, typing_net_wpm, typing_accuracy, part2_grade, maths_score, popi_score, total_score, final_grade, part1_data, p2_typed, p2_target, math_data, popi_data)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (d.get('username'), selected_book, d.get('audio_cps'), d.get('audio_accuracy'), part1_grade,
               p2_gross, p2_net, p2_acc, part2_grade, maths_score, popi_score, total_score, final_grade,
               json.dumps(d.get('part1_data', [])), d.get('p2_typed'), d.get('p2_target'), 
               json.dumps(math_user_answers), json.dumps(popi_user_answers)))
    conn.commit()
    conn.close()

    pdf_filename = f"uploads/{d.get('username', 'Candidate').replace(' ', '_')}_results.pdf"
    generate_combined_pdf(d, pdf_filename)

    return jsonify({'success': True, 'total_score': total_score, 'final_grade': final_grade})

if __name__ == '__main__':
    app.run(debug=True)
