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
            max-width: 700px;
            width: 100%;
            background: #fff;
        }}
        /* LEFT-ALIGNED Optum logo with LOTS of padding */
        .logo-container {{
            width: 100%;
            background: #fff;
            padding: 50px 100px 40px 100px;
            box-sizing: border-box;
        }}
        .logo-text {{
            font-family: Arial, sans-serif;
            font-size: 52px;
            font-weight: bold;
            color: #FF6F00;
            margin: 0;
            text-align: left;
        }}
        .peach-header {{
            width: 100%;
            background-color: #FDEBD0;
            padding: 60px 100px;
            box-sizing: border-box;
        }}
        .peach-content {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 60px;
        }}
        .peach-text {{
            flex: 1;
            text-align: left;
        }}
        .peach-text h2 {{
            color: #000000;
            font-size: 40px;
            font-weight: bold;
            margin: 0;
            line-height: 1.2;
        }}
        .peach-right {{
            flex: 0 0 auto;
        }}
        .susan-image {{
            width: 180px;
            height: 180px;
            border-radius: 50%;
            object-fit: cover;
        }}
        .image-placeholder {{
            width: 180px;
            height: 180px;
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
        /* LOTS of padding for main content */
        .main-content {{
            padding: 60px 100px;
            background: #fff;
        }}
        .main-content h1 {{
            color: #00338D;
            font-size: 38px;
            font-weight: bold;
            margin: 0 0 36px 0;
            text-align: left;
            line-height: 1.3;
        }}
        .description {{
            color: #333333;
            font-size: 16px;
            margin: 0 0 44px 0;
            text-align: left;
            line-height: 1.7;
        }}
        .main-content .greeting {{
            color: #00338D;
            font-size: 19px;
            font-weight: bold;
            margin: 0 0 24px 0;
            text-align: left;
        }}
        .main-content .summary {{
            color: #333333;
            font-size: 16px;
            margin: 0 0 44px 0;
            text-align: left;
            line-height: 1.8;
        }}
        .signature {{
            margin: 0;
            color: #333333;
            font-size: 16px;
            text-align: left;
            line-height: 1.6;
        }}
        /* Dashboard section with LOTS of padding */
        .dashboard-wrapper {{
            padding: 0 100px 60px 100px;
            background: #fff;
        }}
        .dashboard-section {{
            background: #D4F1F4;
            border-radius: 20px;
            padding: 56px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-sizing: border-box;
            gap: 40px;
        }}
        .dashboard-info {{
            flex: 1;
        }}
        .dashboard-info h2 {{
            color: #00338D;
            font-size: 32px;
            font-weight: bold;
            margin: 0 0 20px 0;
        }}
        .dashboard-info p {{
            color: #00338D;
            font-size: 16px;
            margin: 0 0 32px 0;
            line-height: 1.6;
        }}
        .dashboard-button {{
            display: inline-block;
            padding: 16px 48px;
            background: #fff;
            border: 2px solid #00338D;
            border-radius: 32px;
            color: #00338D;
            font-size: 17px;
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
            width: 260px;
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
                <!-- LEFT-ALIGNED BOLD ORANGE Optum logo with MASSIVE padding -->
                <div class="logo-container">
                    <div class="logo-text">Optum</div>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <!-- Peach header with LOTS of padding -->
                <div class="peach-header">
                    <div class="peach-content">
                        <div class="peach-text">
                            <h2>Meet Susan,<br>Your Agile AI<br>Consultant</h2>
                        </div>
                        <div class="peach-right">
                            <!-- Circular image placeholder -->
                            <img src="cid:susan_image" alt="Susan" class="susan-image" style="display:none;">
                            <div class="image-placeholder">Susan's Photo</div>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <!-- Main content with MASSIVE padding -->
                <div class="main-content">
                    <h1>Empowering teams with faster AI Insights.</h1>
                    
                    <div class="description">
                        Susan, your Agile AI Executive Consultant reviews team performance metrics to surface actionable insights across focus areas such as backlog health, sprint health and post-sprint process improvement, helping you identify blockers early. It also recommends next best actions, such as improving refinement of backlog items or rebalancing workload, to optimize sprint outcomes and boost overall team efficiency.
                    </div>
                    
                    <div class="greeting">{greeting}</div>
                    <div class="summary">{limited_html}</div>
                    
                    <!-- ONLY ONE signature -->
                    <div class="signature">Best regards,<br>Susan</div>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <!-- Dashboard section with LOTS of padding -->
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
    AGGRESSIVE DUPLICATE SIGNATURE PREVENTION.
    """
    chart_summary = f"Rally Analysis Summary for {product_manager if product_manager else 'Global Head'}:"
    prompt = (
        "You are Susan, a friendly AI chatbot for Agile teams. "
        "Write a concise summary (3-4 lines MAXIMUM) of the team's performance, backlog health, sprint health, and any blockers or next best actions. "
        "\n\n"
        "ABSOLUTE REQUIREMENTS - VIOLATING THESE WILL CAUSE ERRORS:\n"
        "1. DO NOT write 'Best regards' ANYWHERE in your response\n"
        "2. DO NOT write 'Sincerely' ANYWHERE in your response\n"
        "3. DO NOT write 'Thank you' ANYWHERE in your response\n"
        "4. DO NOT write 'Regards' ANYWHERE in your response\n"
        "5. DO NOT write 'Susan' at the end of your response\n"
        "6. DO NOT include ANY closing statement or sign-off\n"
        "7. END your response immediately after stating the next actions\n"
        "8. The signature 'Best regards, Susan' will be automatically added by the system\n"
        "\n"
        "Your response should end with the actionable recommendations. Nothing more. "
        "Example ending: '...Next steps include prioritizing tasks and improving workflow efficiency.' [STOP HERE]"
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
        
        # AGGRESSIVE cleanup: Remove ANY closing phrases
        closing_phrases = [
            "best regards", "best regard", "regards", "regard",
            "sincerely", "sincere",
            "thank you", "thanks",
            "cheers",
            "warm regards", "kind regards",
            "yours", "cordially",
            "\nsusan", "\n- susan", "\n-susan",
            "respectfully",
            "gratefully"
        ]
        
        response_lower = response.lower()
        
        # Find the earliest occurrence of any closing phrase
        earliest_pos = len(response)
        for phrase in closing_phrases:
            pos = response_lower.find(phrase)
            if pos != -1 and pos < earliest_pos:
                earliest_pos = pos
        
        # Truncate if any closing phrase was found
        if earliest_pos < len(response):
            response = response[:earliest_pos].strip()
        
        # Remove trailing punctuation that might indicate a sign-off
        while response.endswith((',', '-', ':')):
            response = response[:-1].strip()
        
        return response
    except Exception as e:
        return "Unable to generate analysis at this time."


def send_email_with_inline_images(smtp_server, sender_email, recipients, subject, html_content, dashboard_image_path=None, susan_image_path=None):
    """
    Send email with HTML content and optional images.
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
    
    return msg


if __name__ == "__main__":
    print("Rally Email Template - MAXIMUM PADDING VERSION")
    print("=" * 50)
    print("\nPadding applied:")
    print("  Logo: 100px left/right")
    print("  Peach header: 100px all sides")
    print("  Main content: 100px left/right")
    print("  Dashboard: 100px left/right")
    print("\nDuplicate signature prevention: AGGRESSIVE")
