from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen.canvas import Canvas
import json

class GenerateFromTemplate:
    def __init__(self,template):
        self.template_pdf = PdfReader(open(template, "rb"))
        self.template_page= self.template_pdf.pages[0]

        self.packet = io.BytesIO()
        self.c = Canvas(self.packet,pagesize=(self.template_page.mediabox.width,self.template_page.mediabox.height))
        self.c.setFont("Helvetica",18)

    
    def addText(self,text,point):
        self.c.drawString(point[0],point[1],text)

    def merge(self):
        self.c.save()
        self.packet.seek(0)
        result_pdf = PdfReader(self.packet)
        result = result_pdf.pages[0]

        self.output = PdfWriter()

        self.template_page.merge_page(result)
        self.output.add_page(self.template_page)
    
    def generate(self,dest):
        outputStream = open(dest,"wb")
        self.output.write(outputStream)
        outputStream.close()


with open("test.json") as f:
    input_data = json.load(f)


with open("overlay.json") as f:
    overlay_data = json.load(f)

input_arr =  list(input_data.values())
overlay_arr = list(overlay_data.values())

gen = GenerateFromTemplate("test.pdf")

for i in range(len(input_arr)):
    gen.addText(input_arr[i],overlay_arr[i])

gen.merge()
gen.generate("Output.pdf")