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

import string
import unicodedata
from unicodedata import normalize

class PDF2Text:
    def __init__(self):
        self.input = '' # Input directory
        self.output = '' # Output directory
        self.mapping = {}

    def getTXT(self):
        for PDFfile in Path(self.input).glob('*.pdf'):
            inPDFfile = os.path.split(PDFfile)
            lenfilename = inPDFfile[-1].rfind('.')
            outTXTfile = self.output + '\\' + inPDFfile[-1][:lenfilename] + '.txt'
            self.pdf2txt(PDFfile, outTXTfile)

    def pdf2txt(self, inPDFfile, outTXTfile):
        inFile = open(inPDFfile, 'rb')
        resMgr = PDFResourceManager()
        retData = StringIO()
        txtConverter = TextConverter(resMgr, retData, laparams=LAParams())
        interpreter = PDFPageInterpreter(resMgr, txtConverter)
        for page in PDFPage.get_pages(inFile):
            interpreter.process_page(page)
        txt = retData.getvalue()
        txt = self.uncp1252(txt)
        txt = self.transformASCII(txt)
        with open(outTXTfile, 'w', encoding='utf-8') as f:
            f.write(txt)
            print(txt)

    def clean_marks_latin(self, txt):
        norm_txt = unicodedata.normalize('NFD', txt)
        latin_base = False
        remainders = []
        for char in norm_txt:
            if unicodedata.combining(char) and latin_base:
                continue
            remainders.append(char)
            if not unicodedata.combining(char):
                latin_base = char in string.ascii_letters
        trimmed = ''.join(remainders)
        return unicodedata.normalize('NFC', trimmed)

    def uncp1252(self, txt):
        return txt.translate(self.mapping)

    def transformASCII(self, txt):
        cleaned = self.clean_marks_latin(self.uncp1252(txt))
        return unicodedata.normalize('NFKC', cleaned)

oPDF2Text = PDF2Text()
oPDF2Text.getTXT()
