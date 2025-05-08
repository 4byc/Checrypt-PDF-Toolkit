import os
import sys
import pikepdf
from tkinter import filedialog
from checrypt.utils import parse_pages

def split_by_ranges(pdf, ranges, output_dir):
    writers = []
    for r in ranges:
        writer = pikepdf.Pdf.new()
        for page_num in r:
            writer.pages.append(pdf.pages[page_num-1])
        path = os.path.join(output_dir, f"split_{r[0]}-{r[-1]}.pdf")
        writer.save(path)
        writers.append(path)
    return writers

def split_by_size(pdf, max_size, output_dir):
    writers = []
    current = pikepdf.Pdf.new()
    size = 0
    for page in pdf.pages:
        current.pages.append(page)
        size += sys.getsizeof(page)
        if size >= max_size:
            path = os.path.join(output_dir, f"split_{len(current.pages)}.pdf")
            current.save(path)
            writers.append(path)
            current = pikepdf.Pdf.new()
            size = 0
    if current.pages:
        path = os.path.join(output_dir, "split_final.pdf")
        current.save(path)
        writers.append(path)
    return writers

def split_pdf(file_path, split_type, args, cli_mode=False):
    pdf = pikepdf.open(file_path)
    output_dir = args.output_dir if cli_mode else filedialog.askdirectory()
    if split_type == 'range':
        ranges = [list(range(r[0], r[1]+1)) for r in parse_pages(args.ranges)]
        return split_by_ranges(pdf, ranges, output_dir)
    else:
        max_size = float(args.size)*1024*1024
        return split_by_size(pdf, max_size, output_dir)
