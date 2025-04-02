# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pypdf import PdfWriter,PdfReader
import os


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


def find_pdf_files():
    pdf_files = []
    for filename in os.listdir():
        if filename.endswith('.pdf'):
            pdf_files.append(filename)

    pdf_files.sort()
    return pdf_files


# merge all the pdf files to one file
def merge_pdf_files(pdf_files):
    merger = PdfWriter()

    for pdf_file in pdf_files:
        merger.append(pdf_file)

    merger.write("merged-pdf.pdf")
    merger.close()

#1 get all the pdf files in one specific folder
#2 read the files and merge them into one pdf files



