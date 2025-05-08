import pikepdf
from tkinter import filedialog

def merge_pdfs(file_list, cli_mode=False):
    pdf = pikepdf.Pdf.new()
    for f in file_list:
        src = pikepdf.open(f)
        pdf.pages.extend(src.pages)
    if cli_mode:
        out = "merged.pdf"
    else:
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    pdf.save(out)
    return out
