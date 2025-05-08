import os
import pikepdf
from tkinter import filedialog, messagebox
from threading import Event

def bypass_password(file_path, wordlist_path, progress_callback, cancel_event, cli_mode=False):
    if not os.path.exists(file_path) or not os.path.exists(wordlist_path):
        raise FileNotFoundError
    with open(wordlist_path, 'r', encoding='latin-1') as f:
        pwds = f.read().splitlines()
    total = len(pwds)
    for idx, pwd in enumerate(pwds, 1):
        if cancel_event.is_set():
            return None
        progress_callback(idx/total, pwd)
        try:
            pdf = pikepdf.open(file_path, password=pwd)
            if cli_mode:
                out = 'bypassed.pdf'
            else:
                out = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF Files','*.pdf')])
            pdf.save(out)
            return pwd, out
        except pikepdf.PasswordError:
            continue
    return None
