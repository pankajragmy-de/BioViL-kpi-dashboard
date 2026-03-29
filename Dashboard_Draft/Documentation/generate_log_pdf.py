import markdown
import os

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_MD = os.path.join(DOCS_DIR, "BioViL_Development_Log_v1.md")
LOG_HTML = os.path.join(DOCS_DIR, "BioViL_Development_Log_v1.html")
LOGO_PATH = "/Users/pankajsharma/Library/CloudStorage/OneDrive-Personal/AI Agents/Bioenergy_KPI_Dashboard/Logo/logo 1colour  bg w.svg"

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }

@page {
    size: A4;
    margin: 20mm 20mm 20mm 20mm;
}

body {
    font-family: Arial, Helvetica, sans-serif;
    color: #000;
    line-height: 1.5;
    font-size: 11pt;
    background: #fff;
}

.container {
    padding: 0;
}

h1 { font-size: 18pt; margin: 20px 0 10px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
h2 { font-size: 14pt; margin: 15px 0 10px; }
h3 { font-size: 12pt; margin: 10px 0 5px; }
p { margin-bottom: 15px; }
ul, ol { margin-bottom: 15px; padding-left: 20px; }
li { margin-bottom: 5px; }
strong { font-weight: bold; }
em { font-style: italic; }

code {
    font-family: Courier, monospace;
    font-size: 10pt;
}

pre {
    background: #f4f4f4;
    padding: 10px;
    border: 1px solid #ddd;
    margin: 15px 0;
}

hr {
    border: 0;
    height: 1px;
    background: #ccc;
    margin: 20px 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
}
th {
    border-bottom: 2px solid #666;
    padding: 6px;
    text-align: left;
}
td {
    padding: 6px;
    border-bottom: 1px solid #ccc;
}

blockquote {
    border-left: 3px solid #666;
    padding: 10px 15px;
    margin: 15px 0;
    color: #444;
}

img {
    max-width: 100%;
    height: auto;
}
"""

def generate():
    with open(LOG_MD, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Convert markdown to HTML (enable tables and fenced code blocks)
    html_content = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])

    # Fix the logo path if it was converted to an img tag with relative/broken path
    # But since it's an absolute path in the MD, it works in Chrome rendering.

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>BioViL Development Log</title>
    <style>{CSS}</style>
</head>
<body>
<div class="container">
    {html_content}
</div>
</body>
</html>"""

    with open(LOG_HTML, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("✓ Development Log HTML generated")

if __name__ == "__main__":
    generate()
