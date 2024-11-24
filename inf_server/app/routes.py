from myapp import app
from app.inference import handle_img
import os




@app.route('/ask_abadi', methods=['POST'])
def ask_abadi():
    
    f = request.files['file']

    pathname = f"img_file{os.getpid()}.jpg"

    f.save(pathname)
    

    if not handle_img(pathname):
        return {"error": "shit"}, 400

    return {"msg":"shitma balls"}, 200