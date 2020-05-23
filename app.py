import os
from flask import Flask, flash, request, redirect, url_for, session, jsonify, make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
from flask_restful import Resource, Api
#import imageProcess
import plateProcess
import subprocess
from subprocess import Popen
import string

#logging information
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('LOG INFO: ')

#file types
UPLOAD_FOLDER = '/srv/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#app prep
app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
#app.config['CORS_HEADERS'] = 'Content-Type'
#cors = CORS(app, resources={r"/upload": {"origins": "http://localhost:port"}})
CORS(app)

@app.route('/upload', methods=['POST', 'GET'])
#@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def fileUpload():
    if request.method == 'POST':
        target=os.path.join(UPLOAD_FOLDER,'')
        if not os.path.isdir(target):
            os.mkdir(target)
            logger.info("welcome to upload") #upload`
        file = request.files['file'] 
        filename = secure_filename(file.filename)
        destination="".join([target, filename])
        file.save(destination)
        session['uploadFilePath']=destination
        logger.info(destination)
        logger.info(filename)
        #text = imageProcess.processPlate(destination, filename)
        try:
            text = plateProcess.plateProcessor('upload/'+filename)
        except Exception as error:
            print('Caught this error: ' + repr(error))
            logger.info(error)
        os.remove('upload/'+filename)
        logger.info(text)
        data = {'message': 'Successfully loaded', 'text': text} #response="Whatever you wish too return"
        return make_response(jsonify(data), 201)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False, ssl_context='adhoc')

flask_cors.CORS(app, expose_headers='Authorization')