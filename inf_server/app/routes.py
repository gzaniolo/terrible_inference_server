from myapp import app
from flask import request, jsonify
from app.inference import handle_img
import os




@app.route('/ask_abadi', methods=['POST'])
def ask_abadi():
    
    f = request.files['file']
    texts = request.json.get('texts')

    pathname = f"img_file{os.getpid()}.jpg"

    f.save(pathname)
    
    out_dic = handle_img(pathname, texts)

    return jsonify(out_dic), 200