from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # This will enable CORS on all routes

TRUECAPTCHA_USERID = "Alvish"
TRUECAPTCHA_APIKEY = "zH29k4ht5R8UWhpFifO8"

@app.route('/solve-truecaptcha', methods=['POST'])
def solve_truecaptcha():
    data = request.get_json()
    print("Received data:", data)

    image_content = data.get('imageContent')
    if not image_content:
        return jsonify({"result": ""}), 400

    try:
        response = requests.post(
            "https://api.apitruecaptcha.org/one/gettext",
            json={
                "userid": TRUECAPTCHA_USERID,
                "apikey": TRUECAPTCHA_APIKEY,
                "data": image_content
            },
            headers={"Content-Type": "application/json"}
        )
        print("TrueCaptcha response:", response.text)

        if response.status_code != 200:
            return jsonify({"result": ""}), 500

        tc_result = response.json()
        captcha_text = tc_result.get("result", "")
        return jsonify({"result": captcha_text})

    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"result": ""}), 500

if __name__ == '__main__':
    app.run(port=5000)
