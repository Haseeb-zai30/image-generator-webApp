from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Azure OpenAI config
ENDPOINT = "https://mohdh-mf00qotj-swedencentral.openai.azure.com/"
DEPLOYMENT = "dall-e-3"
API_VERSION = "2024-02-01"
API_KEY = os.getenv("AZURE_OPENAI_KEY", "Ebwpx525nsznkK92FvbEoLgycVYWHabdNL1dryk209D2Neyrj1hMJQQJ99BHACfhMk5XJ3w3AAAAACOGexAy")

URL = f"{ENDPOINT}openai/deployments/{DEPLOYMENT}/images/generations?api-version={API_VERSION}"

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    if request.method == "POST":
        prompt = request.form["prompt"]

        headers = {
            "Content-Type": "application/json",
            "api-key": API_KEY
        }

        body = {
            "prompt": prompt,
            "size": "1024x1024",
            "n": 1,
            "style": "vivid",
            "quality": "standard"
        }

        response = requests.post(URL, headers=headers, json=body)
        result = response.json()

        try:
            image_url = result["data"][0]["url"]
        except Exception as e:
            image_url = None
            print("Error:", result)

    return render_template("index.html", image_url=image_url)


if __name__ == "__main__":
    app.run(debug=True)
