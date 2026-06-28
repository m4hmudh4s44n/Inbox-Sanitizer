# 🎣 Inbox-Sanitizer: AI-Powered Phishing Triage Engine

Inbox-Sanitizer is an automated Python security tool designed for **Level-1 SOC Triage**. It connects securely to an inbox via IMAP, pulls unread messages, extracts their content, and passes them to an advanced Language Model (LLM) to calculate a phishing probability score ($0-100\%$) alongside deep analytical reasoning.

---

## ✨ Features
- **Automated Mail Fetching:** Targets unread (`UNSEEN`) messages via secure IMAP connections. 📬
- **Robust Email Parsing:** Decodes complicated headers and extracts raw plaintext bodies from multipart emails. 📝
- **Intelligent Threat Scoring:** Evaluates psychological triggers, suspicious formatting, and urgency metrics to return a strict $0-100\%$ threat probability. 📊
- **Structured JSON Engine:** Forces the AI to output machine-readable JSON data for reliable parsing without string errors. 🤖
- **Cost-Efficient Analytics:** Utilizes optimized inference pathways (`gpt-4o-mini` or free equivalents) for low-latency triage. ⚡

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.x installed. Install the official OpenAI API client library:
```bash
pip install openai

```

### 2. Configuration

Open the script and configure the following variables inside the script:

* `EMAIL_USER`: Your target email address (e.g., your university email).
* `EMAIL_PASS`: Your **16-character Google App Password** (Do not use your main login password!).
* `IMAP_SERVER`: Set to `"imap.gmail.com"`.
* `client = OpenAI(...)`: Insert your developer API key here.

### 3. Usage

Run the triage application from your terminal:

```bash
python Python Mailer Script.py

```

---

## 🧠 SOC Incident Triage Workflow

The application acts as an automated analyst executing the following pipeline:

1. **Ingest:** Scans the inbox and flags unhandled mail artifacts.
2. **Normalize:** Sanitizes raw bytes, strips multi-part formatting, and prepares a payload package.
3. **Analyze:** Prompts the reasoning engine with a rigid zero-temperature payload to maintain analytical consistency.
4. **Triage:** Categorizes the results cleanly based on risk priority levels:
* **`[HIGH RISK]`** ($\ge 75\%$) $\rightarrow$ Urgent isolation recommended.
* **`[SUSPICIOUS]`** ($40\% - 74\%$) $\rightarrow$ Manual review recommended.
* **`[CLEAN]`** ($< 40\%$) $\rightarrow$ Low probability of malicious intent.



---

## ⚖️ Ethical Use & Disclaimer

This repository is created exclusively for **educational, defensive, and authorized research purposes**. The author is not responsible for any misuse, credential leakage, or unauthorized email access using this software. Always ensure you have explicit authorization before scanning an active inbox.

```
