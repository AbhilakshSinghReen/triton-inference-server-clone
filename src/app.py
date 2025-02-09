from flask import Flask, request, jsonify

import gzip
import io


app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def catch_all(path):
    route = f"/{path}"
    method = request.method
    content_type = request.headers.get("Content-Type", "N/A")
    content_length = request.headers.get("Content-Length", "N/A")
    
    print(f"Route: {route}")
    print(f"Method: {method}")
    print(f"Headers: {request.headers}")
    print(f"Content-Type: {content_type}")
    print(f"Content-Length: {content_length}")
    print("")

    try:
        # Read raw request data
        raw_data = request.get_data()
        
        # Try to decompress using gzip
        with io.BytesIO(raw_data) as byte_stream:
            with gzip.GzipFile(fileobj=byte_stream, mode='rb') as gz_file:
                decompressed_data = gz_file.read()
        
        print("got it")
        return jsonify({"success": True, "decoded_content": decompressed_data.decode('utf-8', errors='replace')})
    
    except Exception as e:
        print("crapped it")
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=False)
