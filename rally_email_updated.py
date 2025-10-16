def create_executive_html_report(data, analysis_results, product_manager=None, recipient_name=None):
    """
    Create HTML email report with a concise summary focused on insights.
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
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }}
        .header {{
            width: 100%;
            height: 100px;
            background: #fff;
            display: flex;
            align-items: center;
            padding: 0 32px;
            border-bottom: 1px solid #eee;
        }}
        .peach-header {{
            width: 100%;
            height: 140px;
            background-color: #FDEBD0;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .peach-icons {{
            display: flex;
            gap: 24px;
        }}
        .peach-icon {{
            width: 64px;
            height: 64px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 44px;
        }}
        .peach-icon.orange {{
            background: #FF6F00;
            color: #fff;
        }}
        .peach-icon.blue {{
            background: #0033A0;
            color: #fff;
        }}
        .main-content {{
            padding: 32px;
            min-height: 300px;
            background: #fff;
        }}
        .main-content h1 {{
            color: #0033A0;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 24px;
            text-align: center;
        }}
        .main-content .greeting {{
            color: #0033A0;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 16px;
            text-align: left;
        }}
        .main-content .summary {{
            color: #000000;
            font-size: 16px;
            margin-bottom: 0;
            text-align: left;
            line-height: 1.6;
        }}
        .dashboard-section {{
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            background: #D9F6FA;
            min-height: 300px;
            padding: 48px;
            border-radius: 18px;
            margin: 32px 0;
            width: 100%;
            box-sizing: border-box;
        }}
        .dashboard-info {{
            flex: 1;
        }}
        .dashboard-info h2 {{
            color: #0033A0;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 12px;
        }}
        .dashboard-info p {{
            color: #0033A0;
            font-size: 16px;
            margin-bottom: 18px;
        }}
        .dashboard-button {{
            width: 276px;
            height: 46px;
            background: #fff;
            border: 2px solid #0033A0;
            border-radius: 24px;
            text-align: center;
            line-height: 46px;
            color: #0033A0;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }}
        .dashboard-chart {{
            flex: 0 0 220px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-left: 32px;
        }}
        .signature {{
            margin-top: 24px;
            color: #000000;
            font-size: 16px;
            text-align: left;
        }}
    </style>
</head>
<body>
    <div style="width:100%;background:#fff;text-align:center;padding:24px 0 0 0;">
        <!-- Optum logo SVG at the very top -->
        <svg width="180" height="52" viewBox="0 0 138 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M0 15.6259C0 6.93619 7.03361 0 15.9766 0C24.9196 0 31.9532 6.93619 31.9532 15.6259C31.9532 24.3157..." fill="#FF6F00"/>
        </svg>
    </div>
    <table class="center-table" align="center" cellpadding="0" cellspacing="0" style="margin:0 auto;max-width:640px;width:100%;background:#fff;box-shadow:0 0 10px rgba(0,0,0,0.05);">
        <tr>
            <td>
                <div class="peach-header">
                    <div class="peach-icons">
                        <span style="font-size:140px;background:#FDEBD0;color:#FDEBD0;border-radius:50%;padding:16px;">&#x1F4CA;</span>
                        <span style="font-size:140px;background:#FDEBD0;color:#FDEBD0;border-radius:50%;padding:16px;">&#x1F4C8;</span>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <div class="main-content">
                    <h1>Empowering teams with faster AI Insights.</h1>
                    <div class="greeting">{greeting}</div>
                    <div class="summary">{limited_html}</div>
                    <div class="signature">
                        Best regards,<br>
                        Susan
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <div style="padding: 0 32px 32px 32px;">
                    <div class="dashboard-section">
                        <div class="dashboard-info">
                            <h2>Agile Dashboard</h2>
                            <p>Review your Dashboard—track progress, backlog health, and team velocity.</p>
                            <a class="dashboard-button" href="{app_url}" target="_blank" rel="noopener noreferrer">Review Dashboard</a>
                        </div>
                        <div class="dashboard-chart">
                            <!-- Dashboard preview image would go here -->
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
    # Compose a minimal prompt for the LLM
    chart_summary = f"Rally Analysis Summary for {product_manager if product_manager else 'Global Head'}:"
    prompt = (
        "You are Susan, a friendly AI chatbot for Agile teams, sending a summary email."
        "Write a concise summary (3-4 lines, no more) of the team's performance, backlog health, sprint health, and any blockers or next best actions."
        "Do not include executive highlights or recommendations."
        "Sign off as Susan."
        "Keep it short, factual, and actionable."
    )
    
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": chart_summary}
    ]
    
    # Use the existing RallyChartAnalyzer for LLM call
    analyzer = RallyChartAnalyzer()
    return analyzer.get_overall_analysis(chart_summary, data)


def send_email_with_inline_images(smtp_server, sender_email, recipients, subject, html_content):
    """
    Send email with HTML content.
    """
    # Email sending logic here
    pass
