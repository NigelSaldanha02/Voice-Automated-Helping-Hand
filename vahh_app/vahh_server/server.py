from flask import Flask, request, jsonify, Response
from logic_main import check_object, start_detection, get_status, get_latest_frame
import threading

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_route():
    text = request.json.get("text", "")
    obj  = check_object(text)
    if obj is None:
        return jsonify({"present": False})
    t = threading.Thread(target=start_detection, args=(obj,), daemon=True)
    t.start()
    return jsonify({"present": True, "object": obj})

@app.route("/status")
def status_route():
    return jsonify({"state": get_status()})

@app.route("/frame")
def frame_route():
    """Returns the latest annotated camera frame as a JPEG."""
    frame = get_latest_frame()
    if frame is None:
        return Response(status=204)  # no content yet
    return Response(frame, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)