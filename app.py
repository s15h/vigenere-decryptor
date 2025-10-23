from flask import Flask, render_template, request

import vigenere.encryptor

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        message = request.form['message']
        shift_size = int(request.form['shift_size'])
        encrypted_message = vigenere.encryptor.caesar(shift_size, message)
        return render_template(
            'encryption.jinja',
            encrypted_message=encrypted_message,
            message=message,
            shift_size=shift_size
        )

    return render_template('encryption.jinja')



if __name__ == '__main__':
    app.run(debug=True)
