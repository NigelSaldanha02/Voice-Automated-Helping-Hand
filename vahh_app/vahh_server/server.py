from flask import Flask, request, jsonify
from logic import check_object, start_detection, get_status

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_route():
    text = request.json.get("text", "")
    obj = check_object(text)

    if obj is None:
        return jsonify({"present": False})

    start_detection(obj)
    return jsonify({"present": True, "object": obj})

@app.route("/status")
def status_route():
    return jsonify({"state": get_status()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)