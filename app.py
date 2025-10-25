from flask import Flask, render_template, request

import vigenere.encryptor
from vigenere.cypher import Cypher

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/cypher/info/', methods=['GET', 'POST'])
def cypher_info():
    if request.method == 'POST':
        cypher = Cypher(request.form['cypher'])
        patterns = cypher.get_repeating_patterns()
        return render_template(
            'cypher_info.jinja',
            cypher=cypher.cypher_text,
            patterns=patterns,
            most_likely_key_sizes=cypher.determine_most_likely_key_sizes()
        )
    return render_template('cypher_info.jinja')


@app.route('/decrypt/vigenere', methods=['GET', 'POST'])
def decrypt_vigenere():
    if request.method == 'POST':
        cypher = request.form['cypher']
        keyword = request.form['keyword']
        decrypted_message = vigenere.encryptor.vigenere(
            vigenere.encryptor.vig_decryptkey(keyword),
            cypher
        )
        return render_template(
            'decrypt_vigenere.jinja',
            decrypted_message=decrypted_message,
            cypher=cypher,
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
