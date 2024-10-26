from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen.canvas import Canvas
import io
import json


class GenerateFromTemplate:
    def __init__(self,template):
        self.template_pdf = PdfReader(open(template, "rb"))
        self.template_page= self.template_pdf.pages[0]
        self.packet = io.BytesIO()
        self.c = Canvas(self.packet,pagesize=(self.template_page.mediabox.width,self.template_page.mediabox.height))
        
    def nextpage(self):
        self.c.showPage()

    def addText(self,text,point):
        self.c.setFont("Helvetica",18)
        self.c.drawString(point[0],point[1],text)
        
    def merge(self):
        self.c.save()
        self.packet.seek(0)
        result_pdf = PdfReader(self.packet)
        lenght = len(result_pdf.pages)
        

        self.output = PdfWriter()
        
        for i in range(lenght):
            result = result_pdf.pages[i]
            self.page = self.template_pdf.pages[i]
            self.page.merge_page(result)
            self.output.add_page(self.page)
    
    
    def generate(self):
        outputStream = io.BytesIO()
        self.output.write(outputStream)
        outputStream.seek(0)
        return outputStream 

#UNCOMMENT BELOW AND COMMENT THE GENERATE FUNCTION ABOVE FOR LOCAL TESTING 

#     def generate(self,dest):
#         outputStream = open(dest,"wb")
#         self.output.write(outputStream)
#         outputStream.close()

# with open("tests.json") as f:
#     input_data = json.load(f)["pages"]

# with open("overlay.json") as f:
#     overlay_data = json.load(f)

# pdf_path = overlay_data["path"]
# num_of_pages = len(input_data)
# overlay_position = overlay_data["postion"]

# gen = GenerateFromTemplate(pdf_path)

# for j in range(len(input_data)):
#     input_arr = list(input_data[j].values())
#     overlay_arr = list(overlay_position[j].values())
#     for i in range(len(input_arr)):
#              gen.addText(input_arr[i],overlay_arr[i])
#     gen.nextpage()    

# gen.merge()
# gen.generate("Output.pdf")