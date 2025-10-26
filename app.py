from flask import Flask, render_template, request

import vigenere.encryptor
from vigenere.cipher import Cipher

app = Flask(__name__)


@app.route('/cipher/info/', methods=['GET', 'POST'])
def cipher_info():
    if request.method == 'POST':
        cipher_input_text = None
        cipher = None
        if 'cipher' in request.form.keys() and request.form['cipher']:
            cipher_input_text = request.form['cipher']
            cipher = Cipher(request.form['cipher'])
        if 'cipher_file' in request.files.keys() and request.files['cipher_file']:
            cipher_file = request.files['cipher_file']
            cipher_text = cipher_file.read().decode('utf-8')
            cipher = Cipher(cipher_text)
        if not cipher:
            return "No cipher provided"
        patterns = cipher.get_repeating_patterns()
        return render_template(
            'cipher_info.jinja',
            cipher=cipher_input_text,
            patterns=patterns[0:30],
            most_likely_key_sizes=cipher.determine_most_likely_key_sizes()[0:10]
        )
    return render_template('cipher_info.jinja')


@app.route('/decrypt/vigenere', methods=['GET', 'POST'])
def decrypt_vigenere():
    if request.method == 'POST':
        cipher_input_text = None
        cipher = None

        if 'cipher' in request.form.keys() and request.form['cipher']:
            cipher_input_text = request.form['cipher']
            cipher = request.form['cipher']

        if 'cipher_file' in request.files.keys() and request.files['cipher_file']:
            cipher_file = request.files['cipher_file']
            cipher = cipher_file.read().decode('utf-8')

        if not cipher:
            return "No cipher provided"

        keyword = request.form['keyword']
        decrypted_message = vigenere.encryptor.vigenere(
            vigenere.encryptor.vig_decryptkey(keyword),
            cipher
        )
        return render_template(
            'decrypt_vigenere.jinja',
            decrypted_message=decrypted_message,
            cipher=cipher_input_text,
           keyword=keyword
        )
    return render_template('decrypt_vigenere.jinja')


@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'GET':
        mode = request.args.get('mode')
        if mode == 'caesar':
            return render_template(
                'partials/caesar_encryption_form.jinja',
                mode=mode
            )
        elif mode == 'vigenere':
            return render_template(
                'partials/vigenere_encryption_form.jinja',
                mode=mode
            )
        return render_template('encryption.jinja')
    if request.method == 'POST':
        mode = request.form['mode']
        if mode == 'caesar':
            return encrypt_caesar()
        if mode == 'vigenere':
            return encrypt_vigenere()
        return "Invalid mode selected"

    return render_template('encryption.jinja')


def encrypt_caesar():
    message = request.form['message']
    shift_size = int(request.form['shift_size'])
    encrypted_message = vigenere.encryptor.caesar(shift_size, message)
    return render_template(
        'partials/caesar_encryption_form.jinja',
        encrypted_message=encrypted_message,
        message=message,
        shift_size=shift_size,
        mode="caesar"
    )


def encrypt_vigenere():
    message = request.form['message']
    keyword = request.form['keyword']
    encrypted_message = vigenere.encryptor.vigenere(keyword, message)
    return render_template(
        'partials/vigenere_encryption_form.jinja',
        encrypted_message=encrypted_message,
        message=message,
        keyword=keyword,
        mode="vigenere"
    )


if __name__ == '__main__':
    app.run(debug=True)
