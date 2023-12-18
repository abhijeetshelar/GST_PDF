from flask import Flask, render_template, request, make_response
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    # Get values from the HTML form
    item_name = request.form['item_name']
    item_value = float(request.form['item_value'])
    gst_percentage = float(request.form['gst_percentage'])

    # Calculate GST
    gst_amount = (gst_percentage / 100) * item_value
    total_amount = item_value + gst_amount

    # Create PDF
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer)

    pdf.drawString(100, 800, f'Item Name: {item_name}')
    pdf.drawString(100, 780, f'Item Value: ₹{item_value:.2f}')
    pdf.drawString(100, 760, f'GST Percentage: {gst_percentage}%')
    pdf.drawString(100, 740, f'GST Amount: ₹{gst_amount:.2f}')
    pdf.drawString(100, 720, f'Total Amount: ₹{total_amount:.2f}')

    pdf.showPage()
    pdf.save()

    # Set response headers
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=gst_bill_{item_name}.pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)
