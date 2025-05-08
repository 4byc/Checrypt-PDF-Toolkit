import os
import pikepdf
from tkinter import filedialog, messagebox

def unlock_pdf(file_path, password, cli_mode=False):
    if not os.path.exists(file_path):
        raise FileNotFoundError("Invalid file path")
    pdf = pikepdf.open(file_path, password=password)
    if cli_mode:
        out = "unlocked.pdf"
    else:
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    pdf.save(out)
    return out
