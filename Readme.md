# Vigenère decryptor
## description
Simple tools for cracking a Vigenère cipher using frequency analysis and Kasiski examination. Built with Flask for the web interface. Available at http://vigenere.s15h.nl/


## install instructions
install dependencies with pip:
`pip install -r requirements.txt`

run the app:
`python app.py`

the application will be available at `http://localhost:5000`

## Docker
Build the Docker image:
```bash
docker build -t vigenere-app .
```

Run the container:
```bash
docker run -p 5000:5000 vigenere-app
```

The application will be available at `http://localhost:5000`

