from flask import Flask, request, jsonify, send_file
from inp_en import stt
from en_kan import en_kn
from kn_tcy import kn_tcy
from tcy_op import tcy_op
import pandas as pd
import os

app = Flask(__name__)
from flask_cors import CORS
CORS(app, resources={r"/translate": {"origins": "http://localhost:3000"}})



UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

df = pd.read_excel(r'C:\Users\Akarsh\Documents\Documents\Code\MiniProject\app\backend\src\data\kn_tcy.xlsx')

@app.route('/translate', methods=['POST'])
def translate_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    input_audio_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_audio_path)
    output_audio_path = os.path.join(OUTPUT_FOLDER, 'output.mp3')

    try:
        en_text = stt(input_audio_path)
        print(f"English Text Extracted From Audio: {en_text}")
        
        if en_text == '':
            return jsonify({"error": "No Text Detected in Input Audio"}), 400
        
        kn_text = en_kn(en_text)
        print(f"Kannada Text Translated From English Text: {kn_text}")

        tcy_text = kn_tcy(kn_text, df)
        print(f"Tulu Text Translated From Kannada Text: {tcy_text}")

        status_code = tcy_op(tcy_text, output_audio_path)
        if status_code != 0:
            return jsonify({"error": "Failed to generate output audio"}), 500

        return send_file(output_audio_path, as_attachment=True, download_name='output.mp3')
    except Exception as e:
        print(f"Error during processing: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(input_audio_path):
            os.remove(input_audio_path)

if __name__ == '__main__':
    app.run(debug=True)