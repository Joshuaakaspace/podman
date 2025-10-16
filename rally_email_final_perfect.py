def create_executive_html_report(data, analysis_results, product_manager=None):
    # --- your existing short summary ---
    def get_short_summary(data, analysis_results, product_manager=None):
        # (keep your RallyChartAnalyzer logic here)
        return "Short, crisp 3–4 line summary from the LLM."

    executive_analysis = get_short_summary(data, analysis_results, product_manager)
    lines = [ln.strip() for ln in executive_analysis.splitlines() if ln.strip()]
    limited_html = '<br>'.join(lines[:4])

    greeting = f"Hello {product_manager}," if product_manager else "Hello,"
    app_url = os.getenv("RALLY_APP_URL", "https://example.com/dashboard")

    # NOTE: replace cid:logo with a PNG you attach as CID when sending
    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Optum AI Insights</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- mobile helper (safe for non-Outlook clients) -->
  <style>@media only screen and (max-width:600px){{ .container {{ width:100%!important; }} .px24{{padding-left:16px!important;padding-right:16px!important}} }}</style>
</head>
<body style="margin:0;padding:0;background:#F3F5F7;">
  <center style="width:100%;background:#F3F5F7;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr><td align="center" style="padding:24px;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" class="container" style="width:600px;max-width:600px;">
          
          <!-- Header (logo bar) -->
          <tr>
            <td align="left" style="background:#ffffff;border-radius:12px 12px 0 0;padding:16px 24px;">
              <img src="cid:logo" width="96" height="auto" alt="Optum" style="display:block;border:0;outline:none;text-decoration:none;">
            </td>
          </tr>

          <!-- Card body -->
          <tr>
            <td style="background:#ffffff;border-radius:0 0 12px 12px;padding:0;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                
                <!-- Hero title + avatar (table, not flex) -->
                <tr>
                  <td class="px24" style="padding:24px;">
                    <table role="presentation" width="100%">
                      <tr>
                        <td valign="middle" align="left" style="padding-right:12px;">
                          <h1 style="margin:0 0 6px 0;font:700 26px/32px Arial,Helvetica,sans-serif;color:#0A2A5E;">
                            Meet Susan, Your Agile AI Consultant
                          </h1>
                          <p style="margin:0;font:14px/20px Arial,Helvetica,sans-serif;color:#334155;">
                            Empowering teams with faster AI insights.
                          </p>
                        </td>
                        <td valign="middle" align="right" width="120">
                          <img src="cid:avatar" width="96" height="96" alt="Susan" style="display:block;border-radius:48px;border:0;">
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>

                <!-- Summary copy -->
                <tr>
                  <td class="px24" style="padding:0 24px 8px 24px;">
                    <p style="margin:0 0 6px 0;font:700 16px/22px Arial,Helvetica,sans-serif;color:#0A2A5E;">{greeting}</p>
                    <p style="margin:0 0 12px 0;font:14px/22px Arial,Helvetica,sans-serif;color:#111827;">
                      {limited_html}
                    </p>
                  </td>
                </tr>

                <!-- CTA (bulletproof with VML) -->
                <tr>
                  <td class="px24" style="padding:0 24px 24px 24px;">
                    <!--[if mso]>
                    <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" href="{app_url}" style="height:44px;v-text-anchor:middle;width:220px;" arcsize="12%" strokecolor="#0F62FE" fillcolor="#0F62FE">
                      <w:anchorlock/>
                      <center style="color:#ffffff;font-family:Arial,sans-serif;font-size:16px;font-weight:bold;">Review Dashboard</center>
                    </v:roundrect>
                    <![endif]-->
                    <!--[if !mso]><!-- -->
                    <a href="{app_url}" style="background:#0F62FE;border:1px solid #0F62FE;border-radius:6px;color:#fff;display:inline-block;font:bold 16px Arial,Helvetica,sans-serif;padding:12px 20px;text-decoration:none;">
                      Review Dashboard
                    </a>
                    <!--<![endif]-->
                    <div style="font:12px/18px Arial,Helvetica,sans-serif;color:#64748B;margin-top:8px;">
                      If the button doesn’t work, paste this URL: <span style="word-break:break-all">{app_url}</span>
                    </div>
                  </td>
                </tr>

                <!-- Feature block with light background -->
                <tr>
                  <td class="px24" style="padding:0 24px 24px 24px;">
                    <table role="presentation" width="100%" style="background:#D9F6FA;border-radius:12px;">
                      <tr>
                        <td style="padding:20px;" valign="top">
                          <h2 style="margin:0 0 8px 0;font:700 18px/24px Arial,Helvetica,sans-serif;color:#0A2A5E;">Agile Dashboard</h2>
                          <p style="margin:0;font:14px/22px Arial,Helvetica,sans-serif;color:#111827;">
                            Review track progress, backlog health, and team velocity.
                          </p>
                        </td>
                        <td align="right" valign="middle" style="padding:20px;" width="160">
                          <img src="cid:chart" width="140" alt="Dashboard preview" style="display:block;border:0;">
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
              © {datetime.date.today().year} Optum • Executive AI Insights
            </td>
          </tr>

        </table>
      </td></tr>
    </table>
  </center>
</body>
</html>"""
    return html
