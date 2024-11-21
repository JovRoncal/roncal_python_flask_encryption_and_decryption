from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# Save the key to a file (or store it securely)
fernet = Fernet(key)

app = Flask(__name__)

# POST /encrypt route for encrypting data
@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json.get('data')  # Get the data from the request body
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Encrypt the data
    encrypted_data = fernet.encrypt(data.encode())

    return jsonify({'encrypted_data': encrypted_data.decode()}), 200

# POST /decrypt route for decrypting data
@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_data = request.json.get('encrypted_data')  # Get the encrypted data
    if not encrypted_data:
        return jsonify({'error': 'No encrypted data provided'}), 400

    try:
        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data.encode()).decode()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'decrypted_data': decrypted_data}), 200

if __name__ == '__main__':
    app.run(debug=True)