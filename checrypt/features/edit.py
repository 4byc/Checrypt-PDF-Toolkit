import os
import pikepdf
from tkinter import filedialog
from checrypt.utils import parse_pages

def edit_pages(file_path, pages_str, action, cli_mode=False):
    if not os.path.exists(file_path):
        raise FileNotFoundError
    pages = parse_pages(pages_str)
    pdf = pikepdf.open(file_path)
    writer = pikepdf.Pdf.new()
    if action == 'delete':
        for idx, page in enumerate(pdf.pages, start=1):
            if idx not in pages:
                writer.pages.append(page)
        out_name = "edited.pdf"
    else:
        for pg in pages:
            writer.pages.append(pdf.pages[pg-1])
        out_name = "extracted.pdf"
    if cli_mode:
        out = out_name
    else:
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    writer.save(out)
    return out
