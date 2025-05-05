import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfReader, PdfWriter
import pikepdf
from tqdm import tqdm
from ttkthemes import ThemedTk
from threading import Thread

class PDFToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Checrypt - PDF Toolkit")
        self.root.geometry("1200x700")
        self.root.minsize(900, 600)
        
        self.dark_mode = False
        self.current_feature = None
        self.selected_files = []
        
        self.setup_ui()
        self.setup_styles()
        self.show_welcome()

    def setup_ui(self):
        # === HEADER ===
        self.header = ttk.Frame(self.root)
        self.header.pack(fill=tk.X)
        
        self.toggle_button = ttk.Button(self.header, text="🌙", command=self.toggle_theme)
        self.toggle_button.pack(side=tk.RIGHT, padx=20, pady=10)
        
        ttk.Label(self.header, text="Checrypt - PDF Toolkit", font=("Segoe UI", 20, "bold")).pack(
            side=tk.LEFT, padx=20, pady=10)

        # === KONTEN UTAMA ===
        self.main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Sidebar
        self.sidebar = ttk.Frame(self.main_container)
        self.main_container.add(self.sidebar, weight=1)
        
        # Konten
        self.content_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.content_frame, weight=3)

        # === SIDEBAR ===
        ttk.Label(self.sidebar, text="Fitur", font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        self.features = [
            ("unlock", "Unlock PDF", "🔑"),
            ("merge", "Merge PDFs", "📚"),
            ("edit", "Edit Pages", "✂️"),
            ("bypass", "Bypass Password", "🔒")
        ]
        
        for feature in self.features:
            btn = ttk.Button(self.sidebar, text=feature[1], compound=tk.TOP,
                           command=lambda f=feature[0]: self.show_feature(f))
            btn.pack(fill=tk.X, padx=20, pady=5)

        # === STATUS BAR ===
        self.status = ttk.Label(self.root, text="Siap", relief=tk.SUNKEN, 
                               font=("Segoe UI", 10), anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_styles(self):
        style = ttk.Style()
        colors = self.get_theme_colors()
        
        style.configure("TFrame", background=colors['bg'])
        style.configure("Header.TFrame", background=colors['header_bg'])
        style.configure("Sidebar.TFrame", background=colors['sidebar_bg'])
        style.configure("Content.TFrame", background=colors['content_bg'])
        
        style.configure("TLabel", foreground=colors['text'], background=colors['bg'])
        style.configure("TButton", font=("Segoe UI", 12), padding=5)
        style.configure("Accent.TButton", background=colors['accent'], 
                      foreground=colors['accent_text'])
        
        style.map("TButton",
                 foreground=[('pressed', 'white'), ('active', 'white')],
                 background=[('pressed', '!disabled', colors['accent']), 
                            ('active', colors['accent_hover'])])

        # Konfigurasi khusus untuk elemen lain
        style.configure("TEntry", fieldbackground=colors['entry_bg'], foreground=colors['text'])
        style.configure("TListbox", background=colors['list_bg'], foreground=colors['text'])
        style.configure("Horizontal.TProgressbar", background=colors['accent'])

    def get_theme_colors(self):
        if self.dark_mode:
            return {
                'bg': '#2d2d2d',
                'header_bg': '#202020',
                'sidebar_bg': '#353535',
                'content_bg': '#3d3d3d',
                'text': '#e0e0e0',
                'accent': '#007acc',
                'accent_text': 'white',
                'accent_hover': '#005a9c',
                'entry_bg': '#4a4a4a',
                'list_bg': '#4a4a4a'
            }
        else:
            return {
                'bg': '#ffffff',
                'header_bg': '#007acc',
                'sidebar_bg': '#f5f5f5',
                'content_bg': '#eeeeee',
                'text': '#333333',
                'accent': '#007acc',
                'accent_text': 'white',
                'accent_hover': '#005a9c',
                'entry_bg': '#ffffff',
                'list_bg': '#ffffff'
            }

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.setup_styles()
        self.refresh_ui()

    def refresh_ui(self):
        # Hancurkan semua widget
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Rebuild UI
        self.setup_ui()
        if self.current_feature:
            self.show_feature(self.current_feature)
        else:
            self.show_welcome()

    def show_welcome(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Selamat Datang di Checrypt", 
                 font=("Segoe UI", 24, "bold"), style="Header.TLabel").pack(pady=50)
        ttk.Label(self.content_frame, text="Pilih fitur dari sidebar untuk memulai", 
                 font=("Segoe UI", 16)).pack()

    def show_feature(self, feature):
        self.current_feature = feature
        self.clear_content()
        
        if feature == "unlock":
            self.show_unlock()
        elif feature == "merge":
            self.show_merge()
        elif feature == "edit":
            self.show_edit()
        elif feature == "bypass":
            self.show_bypass()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # FITUR UNLOCK
    def show_unlock(self):
        frame = ttk.LabelFrame(self.content_frame, text="Unlock PDF", padding=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="File PDF:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.unlock_file = ttk.Entry(frame, width=50)
        self.unlock_file.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Pilih File", command=self.select_unlock_file).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.unlock_pass = ttk.Entry(frame, show="*", width=50)
        self.unlock_pass.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Unlock PDF", command=self.unlock_pdf, 
                  style="Accent.TButton").grid(row=2, column=0, columnspan=3, pady=20)

    def select_unlock_file(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.unlock_file.delete(0, tk.END)
            self.unlock_file.insert(0, path)

    def unlock_pdf(self):
        file_path = self.unlock_file.get().strip()
        password = self.unlock_pass.get().strip()
        
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "File tidak valid!")
            return
            
        try:
            with pikepdf.open(file_path, password=password) as pdf:
                output_dir = os.path.dirname(file_path)
                output_path = os.path.join(output_dir, "unlocked.pdf")
                pdf.save(output_path)
                self.status.config(text=f"File unlocked: {output_path}")
                messagebox.showinfo("Sukses", f"File berhasil di-unlock: {output_path}")
        except pikepdf.PasswordError:
            messagebox.showerror("Error", "Password salah!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # FITUR MERGE
    def show_merge(self):
        frame = ttk.LabelFrame(self.content_frame, text="Merge PDFs", padding=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.merge_list = tk.Listbox(frame, width=60, height=10)
        self.merge_list.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, pady=10)
        ttk.Button(btn_frame, text="Tambah File", command=self.add_merge_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Hapus File", command=self.remove_merge_file).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame, text="Merge PDFs", command=self.merge_pdfs, 
                  style="Accent.TButton").grid(row=2, column=0, columnspan=2, pady=20)

    def add_merge_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if files:
            self.selected_files.extend(files)
            self.update_merge_list()

    def remove_merge_file(self):
        selected = self.merge_list.curselection()
        if selected:
            del self.selected_files[selected[0]]
            self.update_merge_list()

    def update_merge_list(self):
        self.merge_list.delete(0, tk.END)
        for file in self.selected_files:
            self.merge_list.insert(tk.END, os.path.basename(file))

    def merge_pdfs(self):
        if len(self.selected_files) < 2:
            messagebox.showerror("Error", "Pilih minimal 2 file untuk merge!")
            return
            
        try:
            merger = PdfWriter()
            for file in self.selected_files:
                merger.append(file)
                
            output_dir = os.path.dirname(self.selected_files[0])
            output_path = os.path.join(output_dir, "merged.pdf")
            merger.write(output_path)
            merger.close()
            
            self.status.config(text=f"File merged: {output_path}")
            messagebox.showinfo("Sukses", f"File berhasil digabung: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # FITUR EDIT
    def show_edit(self):
        frame = ttk.LabelFrame(self.content_frame, text="Edit Pages", padding=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="File PDF:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.edit_file = ttk.Entry(frame, width=50)
        self.edit_file.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Pilih File", command=self.select_edit_file).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(frame, text="Halaman:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pages_entry = ttk.Entry(frame, width=50)
        self.pages_entry.grid(row=1, column=1, padx=5, pady=5)
        self.pages_entry.insert(0, "Contoh: 1,3,5-7")
        
        self.edit_action = tk.StringVar(value="delete")
        ttk.Radiobutton(frame, text="Hapus", variable=self.edit_action, value="delete").grid(row=2, column=0, pady=5)
        ttk.Radiobutton(frame, text="Ekstrak", variable=self.edit_action, value="extract").grid(row=2, column=1, pady=5)
        
        ttk.Button(frame, text="Proses", command=self.edit_pages, 
                  style="Accent.TButton").grid(row=3, column=0, columnspan=2, pady=20)

    def select_edit_file(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.edit_file.delete(0, tk.END)
            self.edit_file.insert(0, path)

    def edit_pages(self):
        file_path = self.edit_file.get().strip()
        pages_input = self.pages_entry.get().strip()
        action = self.edit_action.get()
        
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "File tidak valid!")
            return
            
        try:
            pages = self.parse_pages(pages_input)
            reader = PdfReader(file_path)
            writer = PdfWriter()
            
            if action == "delete":
                for i in range(len(reader.pages)):
                    if i+1 not in pages:
                        writer.add_page(reader.pages[i])
                output_path = os.path.join(os.path.dirname(file_path), "edited.pdf")
            else:
                for page in pages:
                    writer.add_page(reader.pages[page-1])
                output_path = os.path.join(os.path.dirname(file_path), "extracted.pdf")
                
            with open(output_path, "wb") as f:
                writer.write(f)
                
            self.status.config(text=f"File saved: {output_path}")
            messagebox.showinfo("Sukses", f"File berhasil diproses: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def parse_pages(self, input_str):
        pages = []
        parts = input_str.split(',')
        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.extend(range(start, end+1))
            else:
                pages.append(int(part))
        return pages

    # FITUR BYPASS
    def show_bypass(self):
        frame = ttk.LabelFrame(self.content_frame, text="Bypass Password", padding=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="File PDF:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.bypass_file = ttk.Entry(frame, width=50)
        self.bypass_file.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Pilih File", command=self.select_bypass_file).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(frame, text="Wordlist:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.wordlist_file = ttk.Entry(frame, width=50)
        self.wordlist_file.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Pilih Wordlist", command=self.select_wordlist).grid(row=1, column=2, padx=5, pady=5)
        
        self.progress = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=300)
        self.progress.grid(row=2, column=0, columnspan=3, pady=20)
        
        ttk.Button(frame, text="Mulai Bypass", command=self.start_bypass, 
                  style="Accent.TButton").grid(row=3, column=0, columnspan=3)

    def select_bypass_file(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.bypass_file.delete(0, tk.END)
            self.bypass_file.insert(0, path)

    def select_wordlist(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            self.wordlist_file.delete(0, tk.END)
            self.wordlist_file.insert(0, path)

    def start_bypass(self):
        self.progress["value"] = 0
        file_path = self.bypass_file.get().strip()
        wordlist_path = self.wordlist_file.get().strip()
        
        if not os.path.exists(file_path) or not os.path.exists(wordlist_path):
            messagebox.showerror("Error", "File tidak valid!")
            return
            
        thread = Thread(target=self.bypass_password, args=(file_path, wordlist_path))
        thread.start()

    def bypass_password(self, file_path, wordlist_path):
        try:
            with open(wordlist_path, "r", encoding="latin-1") as f:
                passwords = f.read().splitlines()
                total = len(passwords)
                
                for i, password in enumerate(passwords):
                    self.progress["value"] = (i+1)/total * 100
                    self.root.update_idletasks()
                    
                    try:
                        with pikepdf.open(file_path, password=password):
                            output_path = os.path.join(os.path.dirname(file_path), "bypassed.pdf")
                            with pikepdf.open(file_path, password=password) as pdf:
                                pdf.save(output_path)
                                
                            self.status.config(text=f"Password ditemukan: {password}")
                            messagebox.showinfo("Sukses", f"Password ditemukan: {password}\nFile: {output_path}")
                            return
                    except pikepdf.PasswordError:
                        continue
                        
                messagebox.showwarning("Gagal", "Password tidak ditemukan!")
                self.status.config(text="Password tidak ditemukan")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Terjadi error")

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = PDFToolkit(root)
    root.mainloop()