import io
from django.core.files.base import ContentFile
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def create_pdf(parent):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    # create texts
    textobject = p.beginText()
    # start text at top left of page
    textobject.setTextOrigin(inch, 11*inch)
    # set font and size
    textobject.setFont("Helvetica-Bold", 14)
    textobject.textLine("Parent Information")
    textobject.setFont("Helvetica", 12)
    # write parent data
    parent_fn = f"First Name: {parent.first_name}"
    parent_ln = f"Last Name: {parent.last_name}"
    textobject.textLine(parent_fn)
    textobject.textLine(parent_ln)
    textobject.setFont("Helvetica-Bold", 14)
    textobject.textLine()
    textobject.textLine("Children Information")
    textobject.setFont("Helvetica", 12)
    # if there is a child, write child(ren) data
    if parent.childname_set.count() > 0:
        for child in parent.childname_set.all():
            child_fn = f"First Name: {child.first_name}"
            child_ln = f"Last Name: {child.last_name}"
            child_dob = f"Dob: {child.dob}"
            textobject.textLine(child_fn)
            textobject.textLine(child_ln)
            textobject.textLine(child_dob)
            textobject.textLine()
    else:
        textobject.textLine("There is no child")
    # write created text to canvas
    p.drawText(textobject)
    # close the pdf canvas
    p.showPage()
    p.save()

    buffer.seek(0)
    # get content of buffer
    pdf_data = buffer.getvalue()
    # save to django File object
    file_data = ContentFile(pdf_data)
    ## Name the file; here is the crucial part in saving ##
    file_data.name = f'{parent.last_name}.pdf'
    # save file against parent for later retrieval
    parent.pdf=file_data
    parent.save()
