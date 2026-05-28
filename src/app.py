from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Enterprise CI/CD App Running!"

app.run(host="0.0.0.0", port=5000)
