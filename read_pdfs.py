import os
import glob
from pypdf import PdfReader

pdf_dir = "/Users/pankajsharma/Library/CloudStorage/OneDrive-Personal/AI Agents/Bioenergy_KPI_Dashboard/Resources - Year 1"
pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf")) + glob.glob(os.path.join(pdf_dir, "*.PDF"))

for pdf_file in pdf_files[:5]:
    print(f"--- Reading {os.path.basename(pdf_file)} ---")
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for i in range(min(5, len(reader.pages))):
            text += reader.pages[i].extract_text() + "\n"
        print(text[:2000])
    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")
