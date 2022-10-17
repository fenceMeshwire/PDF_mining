#!/usr/bin/env python3

# Python 3.9.5

# basic_PDF_2_txt.py

# Dependencies
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pathlib import Path
import os

class PDF2Text:
    def __init__(self):
        self.input = '...' # Input directory
        self.output = '...' # Output directory

    def getTXT(self):
        for PDFfile in Path(self.input).glob('*.pdf'):
            inPDFfile = os.path.split(PDFfile)
            lenfilename = inPDFfile[-1].rfind('.')
            outTXTfile = self.output + '\\' + inPDFfile[-1][:lenfilename] + '.txt'
            self.pdf2txt(PDFfile, outTXTfile)

    def pdf2txt(inPDFfile, outTXTfile):
        with open(inPDFfile, 'rb') as infile:
            resMgr = PDFResourceManager()
            retData = StringIO()
            txtConverter = TextConverter(resMgr, retData, laparams=LAParams())
            interpreter = PDFPageInterpreter(resMgr, txtConverter)
            for page in PDFPage.get_pages(infile):
                interpreter.process_page(page)
            txt = retData.getvalue()
            with open(outTXTfile, 'wt', encoding='utf-8') as f:
                f.write(txt)

oPDF2Text = PDF2Text()
oPDF2Text.getTXT()
