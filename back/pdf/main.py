import base64
import jinja2
import pdfkit


class PdfFromHtmlDocument:

    def __init__(self, temp_folder: str, temp_name: str):
        self.temp_folder = temp_folder
        self.temp_name = temp_name

    @property
    def template(self):
        template_loader = jinja2.FileSystemLoader(searchpath=self.temp_folder)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(self.temp_name)
        return template

    @staticmethod
    def image_to_base64(image_path: str):
        encoded = base64.b64encode(open(image_path, "rb").read())
        return ("data:image/jpeg;base64," + str(encoded)[1:]).replace("'", "")

    def to_pdf(self, pdf_path: str, **kwargs):
        html_text = self.template.render(
            **kwargs
        )
        pdfkit.from_string(html_text, pdf_path)
        return pdf_path


if __name__ == '__main__':
    rep = PdfFromHtmlDocument("/Users/kirill/own-projects/freelance/pravo_bot/back/pdf/templates", "report.html")
    stages = [
        {
            "id": 1,
            "button": None,
            "question": "⁉️Есть ли у вас гражданство РФ?",
            "messages": [

            ]
        },
        {
            "id": 12,
            "button": "Да",
            "question": "⁉️Есть ли у вас разрешение на временное проживание (РВП) или вид на жительство (ВНЖ)?",
            "messages": [
                {
                    "id": 1,
                    "text": "По большому счету, обе регистрации дают вам одинаковые права, но с временной регистрацией могут быть проблемы, например, при записи в детский сад или при госпитализации. Поэтому, конечно, лучше оформить постоянную регистрацию, если есть такая возможность. Для этого нужно согласие собственника жилья."
                }
            ]
        }
    ]
    rep.to_pdf(
        pdf_path="pdf.pdf",
        logo=rep.image_to_base64("/Users/kirill/own-projects/freelance/pravo_bot/back/pdf/images/logo.png"),
        title="Title",
        stages=stages
    )