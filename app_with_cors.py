
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from fpdf import FPDF
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as origens

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the PDF generator API!"})

@app.route("/generate-form", methods=["POST"])
def generate_form():
    data = request.get_json()
    title = data.get("title", "Untitled Form")
    questions = data.get("questions", [])

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.multi_cell(0, 10, title)
    pdf.set_font("Arial", size=12)

    for i, q in enumerate(questions):
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"{i + 1}. {q['text']}")
        if q["type"] == "input":
            pdf.cell(0, 10, "_" * 80, ln=True)
        elif q["type"] == "scale":
            scale = " ".join(str(i) for i in range(1, 11))
            pdf.cell(0, 10, scale, ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="form.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
