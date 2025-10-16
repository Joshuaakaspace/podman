import os

def create_executive_html_report(data, analysis_results, product_manager=None, recipient_name=None):
    """
    Create HTML email report with a concise summary focused on insights.
    
    Args:
        data: Rally data
        analysis_results: Analysis results from the LLM
        product_manager: Product manager name (used in greeting if recipient_name not provided)
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
    
    # Greeting - use recipient name if provided, otherwise use product manager name
    if recipient_name:
        greeting = f'Hello {recipient_name},'
    elif product_manager:
        greeting = f'Hello {product_manager},'
    else:
        greeting = 'Hello there,'
    
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
            background: #F5F5F5;
        }}
        .center-table {{
            margin: 0 auto;
            max-width: 640px;
            width: 100%;
            background: #fff;
        }}
        /* LEFT-ALIGNED Optum logo */
        .logo-container {{
            width: 100%;
            text-align: left;
            padding: 40px 0 32px 56px;
            background: #fff;
        }}
        .logo-text {{
            font-family: Arial, sans-serif;
            font-size: 48px;
            font-weight: bold;
            color: #FF6F00;
            margin: 0;
            display: inline-block;
        }}
        .peach-header {{
            width: 100%;
            background-color: #FDEBD0;
            padding: 56px 56px 56px 56px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-sizing: border-box;
        }}
        .peach-text {{
            flex: 0 0 auto;
            text-align: left;
        }}
        .peach-text h2 {{
            color: #000000;
            font-size: 38px;
            font-weight: bold;
            margin: 0;
            line-height: 1.2;
        }}
        .peach-right {{
            flex: 0 0 auto;
            margin-left: 40px;
        }}
        .susan-image {{
            width: 160px;
            height: 160px;
            border-radius: 50%;
            object-fit: cover;
        }}
        .image-placeholder {{
            width: 160px;
            height: 160px;
            border-radius: 50%;
            background: #E8D4BC;
            border: 3px solid #D4C4B0;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #8B7355;
            font-size: 14px;
            font-style: italic;
            text-align: center;
            box-sizing: border-box;
        }}
        /* More padding for main content */
        .main-content {{
            padding: 56px 56px 40px 56px;
            background: #fff;
        }}
        .main-content h1 {{
            color: #00338D;
            font-size: 36px;
            font-weight: bold;
            margin: 0 0 32px 0;
            text-align: left;
            line-height: 1.3;
        }}
        .description {{
            color: #333333;
            font-size: 16px;
            margin: 0 0 40px 0;
            text-align: left;
            line-height: 1.6;
        }}
        .main-content .greeting {{
            color: #00338D;
            font-size: 18px;
            font-weight: bold;
            margin: 0 0 20px 0;
            text-align: left;
        }}
        .main-content .summary {{
            color: #333333;
            font-size: 16px;
            margin: 0 0 36px 0;
            text-align: left;
            line-height: 1.7;
        }}
        .signature {{
            margin: 0;
            color: #333333;
            font-size: 16px;
            text-align: left;
            line-height: 1.6;
        }}
        /* Dashboard section with proper padding */
        .dashboard-wrapper {{
            padding: 0 56px 56px 56px;
            background: #fff;
        }}
        .dashboard-section {{
            background: #D4F1F4;
            border-radius: 16px;
            padding: 48px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-sizing: border-box;
        }}
        .dashboard-info {{
            flex: 1;
            padding-right: 32px;
        }}
        .dashboard-info h2 {{
            color: #00338D;
            font-size: 30px;
            font-weight: bold;
            margin: 0 0 16px 0;
        }}
        .dashboard-info p {{
            color: #00338D;
            font-size: 16px;
            margin: 0 0 28px 0;
            line-height: 1.6;
        }}
        .dashboard-button {{
            display: inline-block;
            padding: 14px 44px;
            background: #fff;
            border: 2px solid #00338D;
            border-radius: 30px;
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
        .dashboard-preview {{
            flex: 0 0 auto;
            width: 240px;
        }}
        .dashboard-preview img {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            display: block;
        }}
    </style>
</head>
<body>
    <table class="center-table" align="center" cellpadding="0" cellspacing="0">
        <tr>
            <td>
                <!-- LEFT-ALIGNED BOLD ORANGE Optum logo -->
                <div class="logo-container">
                    <div class="logo-text">Optum</div>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <!-- Peach header with proper padding -->
                <div class="peach-header">
                    <div class="peach-text">
                        <h2>Meet Susan,<br>Your Agile AI<br>Consultant</h2>
                    </div>
                    <div class="peach-right">
                        <!-- Circular image placeholder or actual image -->
                        <img src="cid:susan_image" alt="Susan" class="susan-image" style="display:none;">
                        <div class="image-placeholder">Susan's Photo</div>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <!-- Main content with proper padding (56px sides) -->
                <div class="main-content">
                    <h1>Empowering teams with faster AI Insights.</h1>
                    
                    <div class="description">
                        Susan, your Agile AI Executive Consultant reviews team performance metrics to surface actionable insights across focus areas such as backlog health, sprint health and post-sprint process improvement, helping you identify blockers early. It also recommends next best actions, such as improving refinement of backlog items or rebalancing workload, to optimize sprint outcomes and boost overall team efficiency.
                    </div>
                    
                    <div class="greeting">{greeting}</div>
                    <div class="summary">{limited_html}</div>
                    
                    <!-- Single signature with proper spacing -->
                    <div class="signature">Best regards,<br>Susan</div>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <!-- Dashboard section with proper padding -->
                <div class="dashboard-wrapper">
                    <div class="dashboard-section">
                        <div class="dashboard-info">
                            <h2>Agile Dashboard</h2>
                            <p>Review your Dashboard—track progress, backlog health, and team velocity.</p>
                            <a class="dashboard-button" href="{app_url}" target="_blank" rel="noopener noreferrer">Review Dashboard</a>
                        </div>
                        <div class="dashboard-preview">
                            <!-- Dashboard preview image -->
                            <img src="cid:dashboard_preview" alt="Dashboard Preview">
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
    CRITICAL: This prompt must prevent the LLM from adding any signature or closing.
    """
    chart_summary = f"Rally Analysis Summary for {{product_manager if product_manager else 'Global Head'}}:"
    prompt = (
        "You are Susan, a friendly AI chatbot for Agile teams, sending a summary email. "
        "Write a concise summary (3-4 lines, no more) of the team's performance, backlog health, sprint health, and any blockers or next best actions. "
        "CRITICAL RULES: "
        "1. Do NOT include any signature, closing, or farewell. "
        "2. Do NOT write 'Best regards', 'Sincerely', 'Thank you', or any similar closing. "
        "3. Do NOT mention Susan's name at the end. "
        "4. End immediately after the actionable recommendations. "
        "5. The signature will be added separately by the system. "
        "Keep it short, factual, and actionable. Just provide the analysis, nothing more."
    )
    
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": chart_summary}
    ]
    
    # Use the existing RallyChartAnalyzer for LLM call
    try:
        from rally_chart_intelligence import RallyChartAnalyzer
        analyzer = RallyChartAnalyzer()
        response = analyzer.get_overall_analysis(chart_summary, data)
        
        # Additional cleanup: Remove any closing phrases the LLM might have added
        closing_phrases = [
            "best regards", "sincerely", "thank you", "regards", 
            "best,", "thanks,", "cheers,", "susan"
        ]
        response_lower = response.lower()
        
        # Find if any closing phrase exists and truncate before it
        for phrase in closing_phrases:
            if phrase in response_lower:
                # Find the position and truncate
                pos = response_lower.find(phrase)
                response = response[:pos].strip()
                break
        
        return response
    except Exception as e:
        return "Unable to generate analysis at this time."


def send_email_with_inline_images(smtp_server, sender_email, recipients, subject, html_content, dashboard_image_path=None, susan_image_path=None):
    """
    Send email with HTML content and optional images.
    
    Args:
        smtp_server: SMTP server details (dict with 'host', 'port', 'user', 'password')
        sender_email: Sender email address
        recipients: List of recipient emails
        subject: Email subject
        html_content: HTML content of the email
        dashboard_image_path: Optional path to dashboard preview image
        susan_image_path: Optional path to Susan's profile image
    """
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    import smtplib
    
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
    
    # Attach Susan's image if provided
    if susan_image_path and os.path.exists(susan_image_path):
        with open(susan_image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<susan_image>')
            img.add_header('Content-Disposition', 'inline', filename='susan_image.jpg')
            msg.attach(img)
        
        # If Susan's image is provided, modify HTML to show it instead of placeholder
        html_content = html_content.replace(
            'style="display:none;"',
            'style="display:block;"'
        ).replace(
            '<div class="image-placeholder">Susan\'s Photo</div>',
            '<div class="image-placeholder" style="display:none;">Susan\'s Photo</div>'
        )
    
    # Send email (add your SMTP logic here)
    # Example:
    # try:
    #     with smtplib.SMTP(smtp_server['host'], smtp_server['port']) as server:
    #         server.starttls()
    #         server.login(smtp_server['user'], smtp_server['password'])
    #         server.send_message(msg)
    #     print(f"Email sent successfully to {', '.join(recipients)}")
    # except Exception as e:
    #     print(f"Failed to send email: {e}")
    
    return msg


# Example usage
if __name__ == "__main__":
    # Sample data
    rally_data = {}
    analysis_results = {}
    
    # Create HTML with PERSONALIZED greeting
    html = create_executive_html_report(
        data=rally_data,
        analysis_results=analysis_results,
        product_manager="Ketan Desai",
        recipient_name=None
    )
    
    print("Email HTML generated successfully!")
    print("\nTo send the email, use:")
    print("""
    send_email_with_inline_images(
        smtp_server={'host': 'smtp.example.com', 'port': 587, 'user': 'user', 'password': 'pass'},
        sender_email="susan@optum.com",
        recipients=["ketan.desai@optum.com"],
        subject="Your Agile Insights Summary",
        html_content=html,
        dashboard_image_path="dashboard_preview.png",
        susan_image_path="susan_profile.jpg"  # Optional
    )
    """)
