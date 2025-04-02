from flask import Flask, request, send_file
from fpdf import FPDF
from textwrap import wrap
import tempfile

app = Flask(__name__)

class FormPDF(FPDF):
    def header(self):
        self.set_font("Times", "B", 28)
        self.set_text_color(107, 76, 59)
        self.cell(0, 30, self.title, ln=True, align="C")
        self.ln(10)

    def add_form(self, form_data):
        margin_x = 50
        margin_y = 80
        form_width = self.w - 2 * margin_x
        padding = 20
        content_width = form_width - 2 * padding
        current_y = margin_y + padding
        start_x = margin_x + padding

        self.set_fill_color(242, 231, 219)
        self.rect(margin_x, margin_y, form_width, self.h - 2 * margin_y, 'F')

        self.set_font("Arial", "", 12)
        self.set_text_color(0)
        line_spacing = 18
        input_height = 24
        block_spacing = 18

        def draw_label(text, y_offset, bold=False):
            self.set_xy(start_x, y_offset)
            if bold:
                self.set_font("Arial", "B", 12)
            else:
                self.set_font("Arial", "", 12)
            wrapped = wrap(text, width=90)
            for line in wrapped:
                self.cell(content_width, line_spacing, line, ln=1)
            return self.get_y()

        def draw_input(y_offset):
            self.rect(start_x, y_offset, content_width, input_height)
            return y_offset + input_height + block_spacing

        def draw_scale(y_offset):
            box_size = 16
            spacing = 10
            scale_x = start_x
            self.set_font("Arial", "", 11)
            for i in range(10):
                self.rect(scale_x, y_offset, box_size, box_size)
                self.text(scale_x + 5, y_offset + box_size - 4, str(i + 1))
                scale_x += box_size + spacing
            return y_offset + box_size + block_spacing

        for q in form_data:
            q_type = q.get("type", "input")
            text = q.get("text", "")
            current_y = draw_label(text, current_y)
            if q_type == "input":
                current_y = draw_input(current_y)
            elif q_type == "scale":
                current_y += 6
                current_y = draw_scale(current_y)

@app.route("/generate-form", methods=["POST"])
def generate_form():
    data = request.json
    title = data.get("title", "Form")
    questions = data.get("questions", [])

    pdf = FormPDF(orientation='P', unit='pt', format='A4')
    pdf.title = title
    pdf.add_page()
    pdf.add_form(questions)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp.name)

    return send_file(tmp.name, as_attachment=True, download_name="generated_form.pdf")

if __name__ == "__main__":
    app.run(debug=True)
