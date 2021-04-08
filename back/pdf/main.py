import base64
import jinja2
import pdfkit


class PdfFromHtmlDocument:

    """
    Simple wrapper between jinja2 and pdfkit.
    ATTENTION!
    You must install wkhtmltopdf before using.
    Linux example: sudo apt-get install wkhtmltopdf
    """
    def __init__(self, temp_folder: str, temp_name: str):
        self.temp_folder = temp_folder
        self.temp_name = temp_name

    @property
    def __template(self):
        template_loader = jinja2.FileSystemLoader(searchpath=self.temp_folder)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(self.temp_name)
        return template

    @staticmethod
    def image_to_base64(image_path: str):
        """
        Method transforms picture to dataUrl.
        Use only this image src for correct transformation to PDF
        """
        encoded = base64.b64encode(open(image_path, "rb").read())
        return ("data:image/jpeg;base64," + str(encoded)[1:]).replace("'", "")

    def to_pdf(self, pdf_path: str, **kwargs):
        """
        pdf_path - pdf target path.
        **kwargs - send your variables, which must be used in HTML template.
        """
        html_text = self.__template.render(
            **kwargs
        )
        pdfkit.from_string(html_text, pdf_path)
        return pdf_path