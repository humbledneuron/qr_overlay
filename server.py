from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS for development

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates/logo.svg')
def logo():
    return render_template('logo.svg')

@socketio.on('qr_code_scanned')
def handle_qr_code(data):
    qr_data = data['data']
    print(f"[DEBUG] QR Code received: {qr_data}")

    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert to base64
    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Emit the image to all clients
    socketio.emit('update_qr_code_image', {'qr_image': img_base64})

@socketio.on('step_completed')
def handle_step_completion(data):
    step_number = data['step']
    scanned_data = data['data']
    print(f"[DEBUG] Step {step_number} completed with data: {scanned_data}")
    # Broadcast the step completion to all connected clients
    socketio.emit('step_completed', {'step': step_number, 'data': scanned_data})

if __name__ == '__main__':
    # socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)