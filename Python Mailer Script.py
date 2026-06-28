import imaplib
import email
from email.header import decode_header
import json
from openai import OpenAI

# --- CONFIGURATION ---
EMAIL_USER = "abcd@gmail.com"  # Your Gmail address
EMAIL_PASS = "xxxx xxxx xxxx xxxx"  # Your Google App Password
IMAP_SERVER = "imap.gmail.com"

# Initialize OpenAI client (it automatically looks for OPENAI_API_KEY environment variable)
# Or pass it explicitly: client = OpenAI(api_key="your-api-key")
client = OpenAI(api_key="YOUR_OPENAI_API_KEY_HERE")

def analyze_with_openai(subject, body):
    """Sends email details to OpenAI to evaluate phishing metrics."""
    
    prompt = f"""
    Analyze the following email for phishing indicators. 
    Provide a phishing probability score between 0 and 100.
    Provide a concise reasoning for your score.

    EMAIL SUBJECT: {subject}
    EMAIL BODY:
    \"\"\"
    {body}
    \"\"\"

    You MUST respond ONLY in the following valid JSON format:
    {{
        "score": <integer_between_0_and_100>,
        "reason": "<your_short_explanation_here>"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using gpt-4o-mini as it is fast and highly cost-efficient
            messages=[
                {"role": "system", "content": "You are an expert SOC Analyst specialized in email threat intelligence."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}, # Forces the model to return valid JSON
            temperature=0.0 # Keep temperature at 0 for consistent security scoring
        )
        
        # Parse the JSON response
        result = json.loads(response.choices[0].message.content)
        return result.get("score", 0), result.get("reason", "No reason provided.")
    
    except Exception as e:
        return 0, f"AI Analysis Error: {str(e)}"

def check_mail():
    # Connect to the Gmail server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    # Search for unread (UNSEEN) emails
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()

    print(f"🔎 Found {len(email_ids)} unread emails to analyze...\n")

    for e_id in email_ids:
        res, msg_data = mail.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Decode Subject Line
                subject_header = msg["Subject"]
                if subject_header:
                    subject, encoding = decode_header(subject_header)[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8", errors="ignore")
                else:
                    subject = "No Subject"
                
                sender = msg.get("From")
                
                # Extract Text Body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            payload = part.get_payload(decode=True)
                            if payload:
                                body = payload.decode(errors="ignore")
                                break
                else:
                    payload = msg.get_payload(decode=True)
                    if payload:
                        body = payload.decode(errors="ignore")

                # --- DISPATCH TO OPENAI ---
                score, reason = analyze_with_openai(subject, body)

                # --- PRINT SOC LOG REPORT ---
                print(f"📬 FROM: {sender}")
                print(f"📝 SUBJECT: {subject}")
                
                # Conditional formatting depending on danger level
                if score >= 75:
                    print(f"🚨 PHISHING SCORE: {score}% [HIGH RISK]")
                elif score >= 40:
                    print(f"⚠️ PHISHING SCORE: {score}% [SUSPICIOUS]")
                else:
                    print(f"🟢 PHISHING SCORE: {score}% [CLEAN]")
                    
                print(f"🤖 AI REASONING: {reason}")
                print("-" * 60)

    mail.close()
    mail.logout()

if __name__ == "__main__":
    check_mail()