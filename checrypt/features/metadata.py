import os
import pikepdf
from tkinter import filedialog

def load_metadata(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError
    pdf = pikepdf.open(file_path)
    info = pdf.docinfo
    return {
        'title': info.get('/Title', ''),
        'author': info.get('/Author', ''),
        'subject': info.get('/Subject', ''),
    }

def save_metadata(file_path, title, author, subject, cli_mode=False):
    if not os.path.exists(file_path):
        raise FileNotFoundError
    pdf = pikepdf.open(file_path)
    info = pdf.docinfo
    info['/Title'] = title
    info['/Author'] = author
    info['/Subject'] = subject
    if cli_mode:
        out = 'modified.pdf'
    else:
        out = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF Files', '*.pdf')])
    pdf.save(out)
    return out
