import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from threading import Event, Thread
import argparse
import sys

from checrypt.features.unlock import unlock_pdf
from checrypt.features.merge import merge_pdfs
from checrypt.features.edit import edit_pages
from checrypt.features.split import split_pdf
from checrypt.features.metadata import load_metadata, save_metadata
from checrypt.features.bypass import bypass_password

class PDFToolkit(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Checrypt - PDF Toolkit")
        self.geometry("1200x700")
        self.minsize(900, 600)
        self.selected_files = []
        self.cancel_event = Event()
        self.cli_mode = False
        self.setup_high_dpi()
        self.setup_styles()
        self.setup_ui()
        self.show_welcome()

    def setup_high_dpi(self):
        if os.name == "nt":
            try:
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass

    def setup_styles(self):
        style = ttk.Style()
        self.tk_setPalette(background='#1c1c1c', foreground='white')
        style.theme_use('default')
        style.configure("TFrame", background='#1c1c1c')
        style.configure("TLabel", background='#1c1c1c', foreground='white')
        style.configure("TButton", background='#333333', foreground='white')
        style.configure("Accent.TButton", background='#4c4c4c', foreground='white')
        style.map("Accent.TButton", background=[('active', '#666666'), ('pressed', '#4c4c4c')])
        style.configure("TEntry", fieldbackground='#2e2e2e', foreground='white')
        style.configure("Horizontal.TProgressbar", background='#4c4c4c')

    def setup_ui(self):
        header = ttk.Frame(self)
        header.pack(fill=tk.X)
        ttk.Label(header, text="Checrypt - PDF Toolkit", font=("Segoe UI", 20, "bold")).pack(side=tk.LEFT, padx=20, pady=10)

        self.main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        sidebar = ttk.Frame(self.main_pane)
        self.main_pane.add(sidebar, weight=1)
        ttk.Label(sidebar, text="Features", font=("Segoe UI", 14, "bold")).pack(pady=15)
        self.features = [
            ("unlock", "Unlock PDF"),
            ("merge", "Merge PDFs"),
            ("edit", "Edit Pages"),
            ("split", "Split PDF"),
            ("metadata", "Edit Metadata"),
            ("bypass", "Bypass Password"),
        ]
        for key, label in self.features:
            btn = ttk.Button(sidebar, text=label, style="Accent.TButton", command=lambda k=key: self.show_feature(k))
            btn.pack(fill=tk.X, padx=20, pady=5)

        self.content = ttk.Frame(self.main_pane)
        self.main_pane.add(self.content, weight=3)

        self.status = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def show_welcome(self):
        self.clear_content()
        ttk.Label(self.content, text="Welcome to Checrypt!", font=("Segoe UI", 24, "bold")).pack(pady=50)
        ttk.Label(self.content, text="Select a feature from the sidebar to get started.", font=("Segoe UI", 16)).pack()

    def show_feature(self, name):
        self.clear_content()
        getattr(self, f"_feature_{name}")()

    def _feature_unlock(self):
        frame = ttk.LabelFrame(self.content, text="Unlock PDF", padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="PDF File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry = ttk.Entry(frame, width=50)
        entry.grid(row=0, column=1, padx=5)
        entry.drop_target_register(DND_FILES)
        entry.dnd_bind('<<Drop>>', lambda e: entry.insert(0, e.data.strip('{}')))
        ttk.Button(frame, text="Browse", command=lambda: entry.insert(0, filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")]))).grid(row=0, column=2)
        ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        pw = ttk.Entry(frame, show="*", width=50)
        pw.grid(row=1, column=1, padx=5)
        ttk.Button(frame, text="Unlock", style="Accent.TButton", command=lambda: self._run_unlock(entry.get(), pw.get())).grid(row=2, column=0, columnspan=3, pady=10)

    def _run_unlock(self, path, password):
        try:
            out = unlock_pdf(path, password, self.cli_mode)
            self.status.config(text=f"Unlocked to {out}")
            messagebox.showinfo("Success", f"Saved: {out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _feature_merge(self):
        frame = ttk.LabelFrame(self.content, text="Merge PDFs", padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        lst = tk.Listbox(frame, width=60, height=10, bg='#2e2e2e', fg='white')
        lst.pack(pady=5)
        lst.drop_target_register(DND_FILES)
        lst.dnd_bind('<<Drop>>', lambda e: [lst.insert(tk.END, p) for p in e.data.split()])
        btn_container = ttk.Frame(frame)
        btn_container.pack(pady=5)
        ttk.Button(btn_container, text="Add Files", command=lambda: [lst.insert(tk.END, f) for f in filedialog.askopenfilenames(filetypes=[("PDF","*.pdf")])]).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_container, text="Merge", style="Accent.TButton", command=lambda: self._run_merge(lst.get(0, tk.END))).pack(side=tk.LEFT, padx=5)

    def _run_merge(self, files):
        try:
            out = merge_pdfs(files, self.cli_mode)
            self.status.config(text=f"Merged to {out}")
            messagebox.showinfo("Success", f"Saved: {out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _feature_edit(self):
        frame = ttk.LabelFrame(self.content, text="Edit Pages", padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="PDF File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry = ttk.Entry(frame, width=50)
        entry.grid(row=0, column=1, padx=5)
        entry.drop_target_register(DND_FILES)
        entry.dnd_bind('<<Drop>>', lambda e: entry.insert(0, e.data.strip('{}')))
        ttk.Button(frame, text="Browse", command=lambda: entry.insert(0, filedialog.askopenfilename(filetypes=[("PDF","*.pdf")]))).grid(row=0, column=2)
        ttk.Label(frame, text="Pages (e.g. 1,3-5):").grid(row=1, column=0, sticky=tk.W, pady=5)
        pages = ttk.Entry(frame, width=50)
        pages.grid(row=1, column=1, padx=5)
        action = tk.StringVar(value="delete")
        ttk.Radiobutton(frame, text="Delete", variable=action, value="delete").grid(row=2, column=0)
        ttk.Radiobutton(frame, text="Extract", variable=action, value="extract").grid(row=2, column=1)
        ttk.Button(frame, text="Run", style="Accent.TButton", command=lambda: self._run_edit(entry.get(), pages.get(), action.get())).grid(row=3, column=0, columnspan=3, pady=10)

    def _run_edit(self, path, pg_str, action):
        try:
            out = edit_pages(path, pg_str, action, self.cli_mode)
            self.status.config(text=f"Processed to {out}")
            messagebox.showinfo("Success", f"Saved: {out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _feature_split(self):
        frame = ttk.LabelFrame(self.content, text="Split PDF", padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="PDF File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry = ttk.Entry(frame, width=50)
        entry.grid(row=0, column=1, padx=5)
        entry.drop_target_register(DND_FILES)
        entry.dnd_bind('<<Drop>>', lambda e: entry.insert(0, e.data.strip('{}')))
        ttk.Button(frame, text="Browse", command=lambda: entry.insert(0, filedialog.askopenfilename(filetypes=[("PDF","*.pdf")]))).grid(row=0, column=2)
        split_type = tk.StringVar(value="range")
        ttk.Radiobutton(frame, text="Ranges", variable=split_type, value="range").grid(row=1, column=0)
        ttk.Radiobutton(frame, text="Size", variable=split_type, value="size").grid(row=1, column=1)
        ranges = ttk.Entry(frame, width=50)
        ranges.grid(row=2, column=1, padx=5)
        ttk.Label(frame, text="Ranges (e.g. 1-5,7-9)").grid(row=2, column=0, sticky=tk.W)
        size = ttk.Entry(frame, width=50)
        size.grid(row=3, column=1, padx=5)
        ttk.Label(frame, text="Max size (MB)").grid(row=3, column=0, sticky=tk.W)
        ttk.Button(frame, text="Run", style="Accent.TButton", command=lambda: self._run_split(entry.get(), split_type.get(), ranges.get(), size.get())).grid(row=4, column=0, columnspan=3, pady=10)

    def _run_split(self, path, stype, ranges_str, size_str):
        class Args: pass
        args = Args()
        args.ranges = ranges_str if stype=="range" else None
        args.size = float(size_str) if size_str else None
        args.output_dir = None
        try:
            outs = split_pdf(path, stype, args, self.cli_mode)
            self.status.config(text=f"Split into {len(outs)} files")
            messagebox.showinfo("Success", f"Created: {outs}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _feature_metadata(self):
        frame = ttk.LabelFrame(self.content, text="Edit Metadata", padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="PDF File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry = ttk.Entry(frame, width=50)
        entry.grid(row=0, column=1, padx=5)
        entry.drop_target_register(DND_FILES)
        entry.dnd_bind('<<Drop>>', lambda e: entry.insert(0, e.data.strip('{}')))
        ttk.Button(frame, text="Browse", command=lambda: entry.insert(0, filedialog.askopenfilename(filetypes=[("PDF","*.pdf")]))).grid(row=0, column=2)
        ttk.Button(frame, text="Load", style="Accent.TButton", command=lambda: self._run_load_meta(entry.get())).grid(row=1, column=0, columnspan=3, pady=5)
        self.meta_title = ttk.Entry(frame, width=50)
        self.meta_author = ttk.Entry(frame, width=50)
        self.meta_subject = ttk.Entry(frame, width=50)
        ttk.Label(frame, text="Title").grid(row=2, column=0, sticky=tk.W)
        self.meta_title.grid(row=2, column=1, padx=5)
        ttk.Label(frame, text="Author").grid(row=3, column=0, sticky=tk.W)
        self.meta_author.grid(row=3, column=1, padx=5)
        ttk.Label(frame, text="Subject").grid(row=4, column=0, sticky=tk.W)
        self.meta_subject.grid(row=4, column=1, padx=5)
        ttk.Button(frame, text="Save", style="Accent.TButton", command=lambda: self._run_save_meta(entry.get())).grid(row=5, column=0, columnspan=3, pady=10)

    def _run_load_meta(self, path):
        try:
            data = load_metadata(path)
            self.meta_title.delete(0, tk.END); self.meta_title.insert(0, data['title'])
            self.meta_author.delete(0, tk.END); self.meta_author.insert(0, data['author'])
            self.meta_subject.delete(0, tk.END); self.meta_subject.insert(0, data['subject'])
            self.status.config(text="Metadata loaded")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _run_save_meta(self, path):
        try:
            out = save_metadata(path, self.meta_title.get(), self.meta_author.get(), self.meta_subject.get(), self.cli_mode)
            self.status.config(text=f"Metadata saved to {out}")
            messagebox.showinfo("Success", f"Saved: {out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _feature_bypass(self):
        frame = ttk.LabelFrame(self.content, text="Bypass Password", padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="PDF File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry = ttk.Entry(frame, width=50)
        entry.grid(row=0, column=1, padx=5)
        entry.drop_target_register(DND_FILES)
        entry.dnd_bind('<<Drop>>', lambda e: entry.insert(0, e.data.strip('{}')))
        ttk.Button(frame, text="Browse", command=lambda: entry.insert(0, filedialog.askopenfilename(filetypes=[("PDF","*.pdf")]))).grid(row=0, column=2)
        ttk.Label(frame, text="Wordlist:").grid(row=1, column=0, sticky=tk.W, pady=5)
        wl = ttk.Entry(frame, width=50)
        wl.grid(row=1, column=1, padx=5)
        wl.drop_target_register(DND_FILES)
        wl.dnd_bind('<<Drop>>', lambda e: wl.insert(0, e.data.strip('{}')))
        ttk.Button(frame, text="Browse", command=lambda: wl.insert(0, filedialog.askopenfilename(filetypes=[("Text","*.txt")]))).grid(row=1, column=2)
        progress = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=300)
        progress.grid(row=2, column=0, columnspan=3, pady=5)
        status = ttk.Label(frame, text="Ready")
        status.grid(row=3, column=0, columnspan=3)
        cancel_btn = ttk.Button(frame, text="Cancel", state=tk.DISABLED, command=lambda: self.cancel_event.set())
        cancel_btn.grid(row=4, column=0, pady=5)
        ttk.Button(frame, text="Start", style="Accent.TButton", command=lambda: self._run_bypass(entry.get(), wl.get(), progress, status, cancel_btn)).grid(row=4, column=1, columnspan=2)

    def _run_bypass(self, path, wordlist, progress, status_lbl, cancel_btn):
        self.cancel_event.clear()
        cancel_btn.config(state=tk.NORMAL)
        def cb(pct, pwd):
            progress['value'] = pct*100
            status_lbl.config(text=f"Trying: {pwd}")
            self.update_idletasks()
        def task():
            try:
                res = bypass_password(path, wordlist, cb, self.cancel_event, self.cli_mode)
                cancel_btn.config(state=tk.DISABLED)
                if res:
                    pwd, out = res
                    messagebox.showinfo("Success", f"Password: {pwd}\nSaved: {out}")
                else:
                    messagebox.showwarning("Failed", "Password not found")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        Thread(target=task, daemon=True).start()
