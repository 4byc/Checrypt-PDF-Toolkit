import os
import pikepdf

def parse_pages(input_str):
    pages = []
    parts = [p.strip() for p in input_str.split(',') if p.strip()]
    if not parts:
        raise ValueError("Specify page numbers or ranges.")
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            if start < 1 or start > end:
                raise ValueError(f"Invalid range: {part}")
            pages.extend(range(start, end+1))
        else:
            num = int(part)
            if num < 1:
                raise ValueError(f"Invalid page number: {part}")
            pages.append(num)
    return sorted(set(pages))
