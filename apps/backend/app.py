from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from the Backend! Version 1.0"

@app.route('/api/data')
def get_data():
    return {"message": "This is backend data", "version": "1.0"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 