import os
from fpdf import FPDF
from PIL import Image
from datetime import datetime
from string import digits
import re

def main():
    """Create a PDF from a directory of images."""
    dir = input("Enter directory path: ")
    if not dir:
        dir = "."
    split_by_timestamp(dir)


def split_by_timestamp(dir):
    """Split input into different groups by timestamp"""
    timestamps = {}
    date = datetime.today().strftime('%Y')
    for filename in os.listdir(dir):
        if ".png" in filename or ".jpg" in filename:
            datepos = filename.find(date)
            if datepos is not -1:
                batch = filename[datepos:-4]
                if batch not in timestamps:
                    timestamps[batch] = []
                timestamps[batch].append(dir + "/" + filename)

    for time, arr in timestamps.items():
        split_by_type(dir, arr, time)


def split_by_type(dir, files, time = ''):
    """Split input into groups by their graph type"""
    types = {}
    # date = datetime.today().strftime('%Y')
    for file in files:

        name = re.sub(r'\d+', '', file)
        name = name[:-4]
        name = name.rstrip('_')
        #name = file[:file.find(date)]
        if name not in types:
            types[name] = []
        types[name].append(file)

    for name, arr in types.items():
        if len(arr) > 1:
            makePdf(name + "_" + time, arr, dir)
        else:
            makePdf(arr[0], arr, dir)


def makePdf(pdfFileName, listPages, dir = ''):
    """Create a PDF from a directory of images."""
    # make pdf_exports folder
    if (dir):
        dir += "/"
        if not os.path.isdir(dir + "/pdf_exports"):
            os.mkdir(dir + "/pdf_exports")
    # determine image size
    cover = Image.open(listPages[0])
    width, height = cover.size

    pdf = FPDF(unit = "pt", format = [width, height])
    # add images one by one to the pdf
    for page in listPages:
        pdf.add_page()
        pdf.image(page, 0, 0)
    # remove path to add pdf_exports
    if pdfFileName.startswith(dir):
        pdfFileName = pdfFileName[len(dir):]
    # create pdf
    pdf.output(dir + "pdf_exports/" + pdfFileName + ".pdf", "F")
if __name__ == "__main__":
    main()

# extra code for different options, single_day allows for creation of one file for one day
# group_by_day allows for grouping images by day rather than exact timestamp

# def group_by_day(dir):
#     timestamps = {}
#     date = datetime.today().strftime('%Y')
#     for filename in os.listdir(dir):
#         if ".png" in filename or ".jpg" in filename:
#             datepos = filename.find(date)
#             if datepos is not -1:
#                 batch = filename[datepos:datepos + 10]
#                 if batch not in timestamps:
#                     timestamps[batch] = []
#                 timestamps[batch].append(dir + "/" + filename)
#
#     for time, arr in timestamps.items():
#         split_by_type(dir, arr, time)


# def single_day(dir):
#     date = input("Enter date (MM/DD/YYYY): ")
#     if not date:
#         date = datetime.today().strftime('%d/%m/%Y')
#
#     date = date.split('/')
#     date = date[2] + '_' + date[0] + '_' + date[1]
#
#     images = []
#     for filename in os.listdir(dir):
#         if date in filename and (".png" in filename or ".jpg" in filename):
#             path = dir + "/" + filename
#             images.append(path)
#     pdfname = date + "_images"
#     if images:
#         makePdf(pdfname, images, dir)
#     else:
#         print("No images from that date found")
