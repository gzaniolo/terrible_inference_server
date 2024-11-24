from myapp import app
from flask import request, jsonify
from app.infer_gd import handle_img
import os




@app.route('/ask_abadi', methods=['POST'])
def ask_abadi():

    f = request.files['file']
    print("Got file")

    texts = request.form.get('texts')
    print("Got texts:", texts)

    pathname = f"img_file{os.getpid()}.jpg"
    f.save(pathname)

    print("Before inference")
    out_dic = handle_img(pathname, texts)
    # out_dic = {"result": "success"}  # Placeholder
    print("After inference")

    return jsonify(out_dic), 200


@app.route('/', methods=['GET'])
def ret():
    return 'ping', 200