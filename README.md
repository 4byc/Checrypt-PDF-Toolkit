
# Checrypt Toolkit 🔐

A lightweight, offline PDF encryption and decryption toolkit with a GUI built in Python using Tkinter.

## 📦 Features

- Encrypt PDF files with a password
- Decrypt password-protected PDFs
- Drag and drop file support
- User-friendly graphical interface (Tkinter)

## 🚀 Getting Started

### Requirements

- Python 3.10+
- Tkinter (usually included with Python)
- PyPDF2

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Run Locally

```bash
python main.py
```

### Build to `.exe`

Install PyInstaller:

```bash
pip install pyinstaller
```

Then:

```bash
pyinstaller --onefile --windowed --name Checrypt --add-data "checrypt;checrypt" main.py
```

## 📁 Folder Structure

```
checrypt/
├── core.py        # Main logic (encrypt/decrypt)
├── gui.py         # Tkinter GUI interface
├── pdf_tools.py   # PDF utilities
├── utils.py       # Helper functions
main.py            # Entry point
```

## 📝 License

MIT License

Copyright (c) 2025 Cheque — 4byc & Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
