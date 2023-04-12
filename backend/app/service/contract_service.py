from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.io.read.types import Decimal


class ContractService:

    @staticmethod
    async def create_contract(order_id: str):

        document = Document()
        page = Page()

        # Setting a layout manager on the Page
        layout = SingleColumnLayout(page)

        # Adding a Paragraph to the Page
        layout.add(Paragraph("Hello World",
                   font_size=Decimal(20), font="Helvetica"))

        document.append_page(page)

        with open("output.pdf", "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, document)
