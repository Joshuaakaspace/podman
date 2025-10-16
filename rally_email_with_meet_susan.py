def create_executive_html_report(data, analysis_results, product_manager=None, recipient_name=None):
    """
    Create HTML email report with a concise summary focused on insights.
    
    Args:
        data: Rally data
        analysis_results: Analysis results from the LLM
        product_manager: Product manager name (optional)
        recipient_name: Recipient's first name for personalized greeting (e.g., "Ketan Desai")
    """
    # Get the short summary
    executive_analysis = get_short_summary(
        data,
        analysis_results,
        product_manager
    )
    
    # Limit to 3-4 non-empty lines
    lines = [ln.strip() for ln in executive_analysis.splitlines() if ln.strip()]
    limited = lines[:4]
    limited_html = '<br>'.join(limited)
    
    # Greeting - use recipient name if provided, otherwise "there"
    greeting = f'Hello {recipient_name},' if recipient_name else 'Hello there,'
    
    # Application URL for the Review Dashboard button
    app_url = os.getenv('RALLY_APP_URL', 'http://wm000189804:8008/')
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=640, initial-scale=1.0">
    <title>Optum AI Insights</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #FFFFFF;
        }}
        .center-table {{
            margin: 0 auto;
            max-width: 640px;
            width: 100%;
            background: #fff;
        }}
        .logo-container {{
            width: 100%;
            text-align: center;
            padding: 32px 0 20px 0;
            background: #fff;
        }}
        .logo-container img {{
            width: 180px;
            height: auto;
        }}
        .peach-header {{
            width: 100%;
            min-height: 280px;
            background-color: #FDEBD0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 40px 48px;
            position: relative;
        }}
        .peach-content {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            max-width: 540px;
            gap: 40px;
        }}
        .peach-text {{
            flex: 1;
            text-align: left;
        }}
        .peach-text h2 {{
            color: #000000;
            font-size: 36px;
            font-weight: bold;
            margin: 0;
            line-height: 1.2;
        }}
        .peach-icons {{
            flex: 0 0 auto;
            display: flex;
            gap: 24px;
            align-items: center;
        }}
        .main-content {{
            padding: 48px 56px;
            background: #fff;
        }}
        .main-content h1 {{
            color: #00338D;
            font-size: 34px;
            font-weight: bold;
            margin: 0 0 28px 0;
            text-align: center;
            line-height: 1.3;
        }}
        .main-content .greeting {{
            color: #00338D;
            font-size: 18px;
            font-weight: bold;
            margin: 0 0 16px 0;
            text-align: left;
        }}
        .main-content .summary {{
            color: #000000;
            font-size: 15px;
            margin: 0 0 28px 0;
            text-align: left;
            line-height: 1.7;
        }}
        .signature {{
            margin: 0;
            color: #000000;
            font-size: 15px;
            text-align: left;
            line-height: 1.6;
        }}
        .dashboard-wrapper {{
            padding: 0 56px 56px 56px;
            background: #fff;
        }}
        .dashboard-section {{
            background: #D4F1F4;
            border-radius: 16px;
            padding: 40px;
            display: table;
            width: 100%;
            box-sizing: border-box;
        }}
        .dashboard-content {{
            display: table-row;
        }}
        .dashboard-info {{
            display: table-cell;
            vertical-align: middle;
            padding-right: 32px;
        }}
        .dashboard-preview {{
            display: table-cell;
            vertical-align: middle;
            width: 220px;
            text-align: right;
        }}
        .dashboard-info h2 {{
            color: #00338D;
            font-size: 28px;
            font-weight: bold;
            margin: 0 0 16px 0;
        }}
        .dashboard-info p {{
            color: #00338D;
            font-size: 15px;
            margin: 0 0 24px 0;
            line-height: 1.6;
        }}
        .dashboard-button {{
            display: inline-block;
            padding: 13px 40px;
            background: #fff;
            border: 2px solid #00338D;
            border-radius: 28px;
            color: #00338D;
            font-size: 16px;
            font-weight: bold;
            text-decoration: none;
            cursor: pointer;
        }}
        .dashboard-button:hover {{
            background: #00338D;
            color: #fff;
        }}
        .dashboard-preview img {{
            max-width: 220px;
            height: auto;
            border-radius: 8px;
            display: block;
        }}
    </style>
</head>
<body>
    <table class="center-table" align="center" cellpadding="0" cellspacing="0">
        <tr>
            <td>
                <!-- Logo at the very top -->
                <div class="logo-container">
                    <svg width="180" height="52" viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg">
                        <text x="10" y="40" font-family="Arial, sans-serif" font-size="36" font-weight="bold" fill="#FF6F00">Optum</text>
                    </svg>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <!-- Peach header with "Meet Susan" text and chart emojis -->
                <div class="peach-header">
                    <div class="peach-content">
                        <div class="peach-text">
                            <h2>Meet Susan,<br>Your Agile AI<br>Consultant</h2>
                        </div>
                        <div class="peach-icons">
                            <div style="font-size: 100px; line-height: 1;">📊</div>
                            <div style="font-size: 100px; line-height: 1;">📈</div>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <!-- Main content -->
                <div class="main-content">
                    <h1>Empowering teams with faster AI Insights.</h1>
                    <div class="greeting">{greeting}</div>
                    <div class="summary">{limited_html}</div>
                    <div class="signature">Best regards,<br>Susan</div>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <!-- Dashboard section - EXACTLY matching desired output -->
                <div class="dashboard-wrapper">
                    <div class="dashboard-section">
                        <div class="dashboard-content">
                            <div class="dashboard-info">
                                <h2>Agile Dashboard</h2>
                                <p>Review your Dashboard—track progress, backlog health, and team velocity.</p>
                                <a class="dashboard-button" href="{app_url}" target="_blank" rel="noopener noreferrer">Review Dashboard</a>
                            </div>
                            <div class="dashboard-preview">
                                <!-- Dashboard preview image -->
                                <img src="cid:dashboard_preview" alt="Dashboard Preview" style="max-width:220px;height:auto;display:block;">
                            </div>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
    </table>
</body>
</html>'''
    
    return html_content


def get_short_summary(data, analysis_results, product_manager=None):
    """
    Compose a minimal prompt for the LLM to generate a concise summary.
    """
    chart_summary = f"Rally Analysis Summary for {product_manager if product_manager else 'Global Head'}:"
    prompt = (
        "You are Susan, a friendly AI chatbot for Agile teams, sending a summary email."
        "Write a concise summary (3-4 lines, no more) of the team's performance, backlog health, sprint health, and any blockers or next best actions."
        "Do not include executive highlights or recommendations."
        "Do NOT include any signature or 'Best regards' - that will be added separately."
        "Keep it short, factual, and actionable."
    )
    
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": chart_summary}
    ]
    
    # Use the existing RallyChartAnalyzer for LLM call
    analyzer = RallyChartAnalyzer()
    return analyzer.get_overall_analysis(chart_summary, data)


def send_email_with_inline_images(smtp_server, sender_email, recipients, subject, html_content, dashboard_image_path=None):
    """
    Send email with HTML content and optional dashboard preview image.
    
    Args:
        smtp_server: SMTP server details
        sender_email: Sender email address
        recipients: List of recipient emails
        subject: Email subject
        html_content: HTML content of the email
        dashboard_image_path: Optional path to dashboard preview image
    """
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    import smtplib
    import os
    
    # Create message
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipients)
    
    # Attach HTML content
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    # Attach dashboard preview image if provided
    if dashboard_image_path and os.path.exists(dashboard_image_path):
        with open(dashboard_image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<dashboard_preview>')
            img.add_header('Content-Disposition', 'inline', filename='dashboard_preview.png')
            msg.attach(img)
    
    # Send email
    # Add your SMTP logic here
    
    return msg
