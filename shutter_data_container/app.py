import requests
from flask import Flask, request
from pathlib import Path
import os

import utils


app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start():

   code: str = request.args.get('code', type=str)
   
   SERVER_URL = f'http://127.0.0.1:8000'
   FILE_URL: str = f'/media/shutter_csv/{code}_shutter.csv'

   response = requests.get(SERVER_URL+FILE_URL)

   # The files folder is in the same folder as this file
   PARENT_FOLDER = Path(__file__).resolve().parent
   FILES_FOLDER: str = os.path.join(PARENT_FOLDER, 'files')
   FILE_PATH: str = os.path.join(FILES_FOLDER, f'{code}_shutter.csv')

   open(FILE_PATH, 'wb').write(response.content)

   # Processing

   utils.clean_folder(FILES_FOLDER)
   
   return str(response.status_code), response.status_code
    


if __name__ == '__main__':
   app.run(
      debug=True,
      host='0.0.0.0',
      port=8004
   )
