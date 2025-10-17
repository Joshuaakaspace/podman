# send_optum_email.py
# Outlook-safe HTML email with big "Optum" wordmark, peach hero, CID images.
import os, ssl, smtplib, mimetypes, datetime
from pathlib import Path
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from string import Template

HERE = Path(__file__).resolve().parent

HTML_TMPL = Template(r"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Optum AI Insights</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    @media only screen and (max-width:600px){
      .container{width:100%!important}
      .px24{padding-left:16px!important;padding-right:16px!important}
    }
  </style>
</head>
<body style="margin:0;padding:0;background:#F3F5F7;">
  <center style="width:100%;background:#F3F5F7;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr><td align="center" style="padding:24px;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" class="container" style="width:600px;max-width:600px;">

          <!-- Header: bigger Optum wordmark -->
          <tr>
            <td align="left" style="background:#ffffff;border-radius:12px 12px 0 0;padding:16px 24px;">
              <span style="font:700 36px/1 Arial,Helvetica,sans-serif;color:#FF6F00;letter-spacing:.2px;">Optum</span>
            </td>
          </tr>

          <!-- Card -->
          <tr>
            <td style="background:#ffffff;border-radius:0 0 12px 12px;padding:0;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">

                <!-- Hero on light peach -->
                <tr>
                  <td class="px24" style="padding:0 24px 0 24px;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                           style="background:#FDEBD0;border-radius:12px;">
                      <tr>
                        <td valign="middle" align="left" style="padding:20px;">
                          <h1 style="margin:0 0 6px 0;font:700 26px/32px Arial,Helvetica,sans-serif;color:#0A2A5E;">
                            Meet Susan, Your Agile AI Consultant
                          </h1>
                          <p style="margin:0;font:14px/20px Arial,Helvetica,sans-serif;color:#334155;">
                            Empowering teams with faster AI insights.
                          </p>
                        </td>
                        <td valign="middle" align="right" width="120" style="padding:20px;">
                          $avatar_img
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>

                <!-- Summary -->
                <tr>
                  <td class="px24" style="padding:16px 24px 8px 24px;">
                    <p style="margin:0 0 6px 0;font:700 16px/22px Arial,Helvetica,sans-serif;color:#0A2A5E;">$greeting</p>
                    <p style="margin:0 0 12px 0;font:14px/22px Arial,Helvetica,sans-serif;color:#111827;">$limited_html</p>
                    <p style="margin:0;font:12px/18px Arial,Helvetica,sans-serif;color:#64748B;">Best regards,<br>Susan</p>
                  </td>
                </tr>

                <!-- CTA (bulletproof for Outlook) -->
                <tr>
                  <td class="px24" style="padding:12px 24px 24px 24px;">
                    <!--[if mso]>
                      <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" href="$app_url"
                        style="height:44px;v-text-anchor:middle;width:220px;" arcsize="12%"
                        strokecolor="#0F62FE" fillcolor="#0F62FE">
                        <w:anchorlock/>
                        <center style="color:#ffffff;font-family:Arial,sans-serif;font-size:16px;font-weight:bold;">
                          Review
                        </center>
                      </v:roundrect>
                    <![endif]-->
                    <!--[if !mso]><!-- -->
                      <a href="$app_url" style="background:#0F62FE;border:1px solid #0F62FE;border-radius:6px;
                         color:#fff;display:inline-block;font:bold 16px Arial,Helvetica,sans-serif;
                         padding:12px 20px;text-decoration:none;">Review</a>
                    <!--<![endif]-->
                    <div style="font:12px/18px Arial,Helvetica,sans-serif;color:#64748B;margin-top:8px;">
                      If the button doesn’t work, paste this URL: <span style="word-break:break-all">$app_url</span>
                    </div>
                  </td>
                </tr>

                <!-- Feature strip with chart -->
                <tr>
                  <td class="px24" style="padding:0 24px 24px 24px;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                           style="background:#D9F6FA;border-radius:12px;">
                      <tr>
                        <td style="padding:20px;" valign="top">
                          <h2 style="margin:0 0 8px 0;font:700 18px/24px Arial,Helvetica,sans-serif;color:#0A2A5E;">
                            Agile Dashboard
                          </h2>
                          <p style="margin:0;font:14px/22px Arial,Helvetica,sans-serif;color:#111827;">
                            Review track progress, backlog health and team velocity.
                          </p>
                        </td>
                        <td align="right" valign="middle" style="padding:20px;" width="160">
                          $chart_img
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>

              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td align="center" style="padding:12px 24px 0 24px;font:12px/18px Arial,Helvetica,sans-serif;color:#94A3B8;">
              © $year Optum • Executive AI Insights
            </td>
          </tr>

        </table>
      </td></tr>
    </table>
  </center>
</body>
</html>""")

def build_html(product_manager=None, summary_lines=None, app_url="https://example.com",
               avatar_cid=None, chart_cid=None) -> str:
    greeting = f"Hello {product_manager}," if product_manager else "Hello,"
    limited_html = "<br>".join((summary_lines or [])[:4]) or "Your weekly executive summary is ready."
    avatar_img = f'<img src="cid:{avatar_cid}" width="96" height="96" alt="Susan" style="display:block;border-radius:48px;border:0;">' if avatar_cid else ""
    chart_img  = f'<img src="cid:{chart_cid}" width="140" alt="Dashboard preview" style="display:block;border:0;">' if chart_cid else ""
    return HTML_TMPL.substitute(
        greeting=greeting,
        limited_html=limited_html,
        app_url=app_url,
        avatar_img=avatar_img,
        chart_img=chart_img,
        year=datetime.date.today().year
    )

# ---------- email helpers ----------
def make_message(subject, sender_name, sender_email, to_emails, html):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = ", ".join(to_emails)
    msg.set_content("View this message in an HTML-capable email client.")
    msg.add_alternative(html, subtype="html")
    return msg

def attach_cid(msg: EmailMessage, path: Path):
    if not path.exists():
        return None
    data = path.read_bytes()
    ctype = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    cid = make_msgid().strip("<>")
    msg.get_payload()[1].add_related(data, maintype=maintype, subtype=subtype, cid=cid)
    return cid

def send_o365(msg: EmailMessage, username: str, password: str):
    with smtplib.SMTP("smtp.office365.com", 587) as s:
        s.starttls(context=ssl.create_default_context())
        s.login(username, password)
        s.send_message(msg)

# ---------- run example ----------
if __name__ == "__main__":
    SMTP_USER = os.getenv("SMTP_USER", "no-reply@yourdomain.com")
    SMTP_PASS = os.getenv("SMTP_PASS", "YOUR_SMTP_PASSWORD")
    TO = ["recipient@example.com"]

    PRODUCT_MANAGER = "Ketan Desai"
    APP_URL = os.getenv("RALLY_APP_URL", "http://wm000189804:8080/")
    SUMMARY_LINES = [
        "Team performance shows a high volume of user stories in 'Refining' with minimal progress.",
        "Backlog health is concerning; many items stagnant.",
        "Sprint health unclear due to lack of active progress.",
        "Next steps: clear ownership and address bottlenecks."
    ]

    # Two PNGs in the same directory
    avatar_file = HERE / "avatar.png"
    dashboard_file = HERE / "dashboard.png"

    # Build initial message
    temp_html = build_html(PRODUCT_MANAGER, SUMMARY_LINES, APP_URL, None, None)
    msg = make_message("Executive AI Insights", "Optum AI Insights", SMTP_USER, TO, temp_html)

    # Attach images and rebuild with real CIDs
    avatar_cid = attach_cid(msg, avatar_file)
    dashboard_cid = attach_cid(msg, dashboard_file)
    final_html = build_html(PRODUCT_MANAGER, SUMMARY_LINES, APP_URL, avatar_cid, dashboard_cid)
    msg.get_payload()[1].set_content(final_html, subtype="html")

    # Send
    send_o365(msg, SMTP_USER, SMTP_PASS)
    print("Sent.")
