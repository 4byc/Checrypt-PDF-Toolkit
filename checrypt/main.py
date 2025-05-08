import sys
import argparse
from checrypt.gui import PDFToolkit
from checrypt.features.unlock import unlock_pdf
from checrypt.features.merge import merge_pdfs
from checrypt.features.edit import edit_pages
from checrypt.features.split import split_pdf
from checrypt.features.metadata import save_metadata
from checrypt.features.bypass import bypass_password

def main():
    parser = argparse.ArgumentParser(description="Checrypt PDF Toolkit CLI")
    subparsers = parser.add_subparsers(dest='cmd')
    pk = subparsers.add_parser('unlock')
    pk.add_argument('-i','--input',required=True)
    pk.add_argument('-p','--password',required=True)
    pm = subparsers.add_parser('merge')
    pm.add_argument('-i','--inputs',nargs='+',required=True)
    ps = subparsers.add_parser('split')
    ps.add_argument('-i','--input',required=True)
    ps.add_argument('-r','--ranges')
    ps.add_argument('-s','--size',type=float)
    pmd = subparsers.add_parser('metadata')
    pmd.add_argument('-i','--input',required=True)
    pmd.add_argument('--title')
    pmd.add_argument('--author')
    pmd.add_argument('--subject')
    pb = subparsers.add_parser('bypass')
    pb.add_argument('-i','--input',required=True)
    pb.add_argument('-w','--wordlist',required=True)

    args = parser.parse_args()
    if args.cmd:
        if args.cmd == 'unlock':
            out = unlock_pdf(args.input, args.password, cli_mode=True)
        elif args.cmd == 'merge':
            out = merge_pdfs(args.inputs, cli_mode=True)
        elif args.cmd == 'split':
            out = split_pdf(args.input, 'range' if args.ranges else 'size', args, cli_mode=True)
        elif args.cmd == 'metadata':
            out = save_metadata(args.input, args.title or '', args.author or '', args.subject or '', cli_mode=True)
        elif args.cmd == 'bypass':
            res = bypass_password(args.input, args.wordlist, lambda p,_:None, None, cli_mode=True)
            out = res[1] if res else None
        print(f"Output: {out}")
    else:
        PDFToolkit().mainloop()

if __name__ == '__main__':
    main()
