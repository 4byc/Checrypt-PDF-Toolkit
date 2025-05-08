# Checrypt

**Checrypt** is a simple, GUI-based PDF security toolkit built with Python and Tkinter. It offers a convenient way to encrypt, decrypt, split, merge, and edit PDF metadata — all in one executable tool.

## 🔧 Features

- 🔐 Unlock encrypted PDFs
- 🔒 Apply password protection
- ✂️ Split PDF into individual pages
- 🧩 Merge multiple PDFs
- 📝 Edit PDF metadata (author, title, etc.)
- 🚫 Bypass restrictions (for non-DRM content)
- ✅ Simple GUI interface (no command line needed)

## 📁 Project Structure

```
Checrypt/
├── build/
│   └── Checrypt/
│       └── localpycs/
├── checrypt/
│   ├── __pycache__/
│   ├── features/
│   │   ├── __init__.py
│   │   ├── bypass.py
│   │   ├── edit.py
│   │   ├── merge.py
│   │   ├── metadata.py
│   │   ├── split.py
│   │   └── unlock.py
│   ├── __init__.py
│   ├── gui.py
│   ├── main.py
│   └── utils.py
├── dist/
│   └── Checrypt.exe
├── Checrypt.spec
├── README.md
├── requirements.txt
└── setup.py
```

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/checrypt.git
cd checrypt
```

### 2. Install Dependencies

> It's recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

### 3. Run the App (Development Mode)

```bash
python checrypt/main.py
```

---

## 📦 Build to Executable (Windows)

Make sure you have `pyinstaller` installed:

```bash
pip install pyinstaller
```

Then run:

```bash
pyinstaller --onefile --windowed --name Checrypt --add-data "checrypt;checrypt" checrypt/main.py
```

The `.exe` will be created in the `dist/` folder.

---

## 📃 License

This project is licensed under the [MIT License](LICENSE) — made with ❤️ by 4byc & team.
