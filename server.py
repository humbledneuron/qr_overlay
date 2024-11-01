from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)
socketio = SocketIO(app)

# Serve the webpage
@app.route('/')
def index():
    return render_template('index.html')

# Handle the event when a QR code is detected
@socketio.on('qr_code_detected')
def handle_qr_code(data):
    qr_data = data['qr_data']
    print(f"[DEBUG] QR Code received: {qr_data}")

    # Generate a QR code image from the received QR code data
    qr_img = qrcode.make(qr_data)

    # Convert the image to a base64-encoded string
    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Broadcast the QR code image (base64) to all connected clients
    socketio.emit('update_qr_code_image', {'qr_image': img_base64})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
