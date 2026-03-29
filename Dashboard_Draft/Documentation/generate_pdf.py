import markdown
from weasyprint import HTML, CSS
import os

def markdown_to_pdf(md_file, pdf_file):
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Convert markdown to HTML
    html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    
    # Add CSS for a very premium corporate layout
    css_content = """
    @page {
        size: A4;
        margin: 2.5cm 2cm;
        @bottom-right {
            content: "Page " counter(page) " of " counter(pages);
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 9pt;
            color: #64748b;
        }
        @bottom-left {
            content: "BioViL Energy KPI Dashboard";
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 9pt;
            color: #64748b;
        }
    }
    body {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        color: #1e293b;
        line-height: 1.6;
        font-size: 11pt;
    }
    h1 {
        color: #0f172a;
        font-size: 24pt;
        border-bottom: 2px solid #10b981;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    h2 {
        color: #334155;
        font-size: 16pt;
        margin-top: 30px;
        margin-bottom: 15px;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 5px;
    }
    h3 {
        color: #10b981;
        font-size: 13pt;
        margin-top: 20px;
    }
    p {
        margin-bottom: 15px;
        text-align: justify;
    }
    ul, ol {
        margin-bottom: 15px;
        padding-left: 25px;
    }
    li {
        margin-bottom: 8px;
    }
    strong {
        color: #0f172a;
    }
    a {
        color: #3b82f6;
        text-decoration: none;
    }
    img {
        max-width: 100%;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin: 20px 0;
    }
    """
    
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{md_file}</title>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    # Render PDF
    HTML(string=full_html, base_url=os.getcwd()).write_pdf(
        pdf_file,
        stylesheets=[CSS(string=css_content)]
    )
    print(f"Successfully generated {pdf_file}")

if __name__ == "__main__":
    markdown_to_pdf("BioViL_Detailed_Report.md", "BioViL_Detailed_Report.pdf")
    markdown_to_pdf("BioViL_One_Pager.md", "BioViL_One_Pager.pdf")
