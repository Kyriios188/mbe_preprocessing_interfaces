import requests
from flask import Flask, request
from pathlib import Path
import os

import fill_database

import utils


app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start():

   code: str = request.args.get('code', type=str)
   
   SERVER_URL = f'http://172.20.0.2:8000'
   FILE_URL: str = f'/media/recipe_layer_number_tdms/{code}_recipe_layer_number.tdms'

   response = requests.get(SERVER_URL+FILE_URL)

   # The files folder is in the same folder as this file
   PARENT_FOLDER = Path(__file__).resolve().parent
   FILES_FOLDER: str = os.path.join(PARENT_FOLDER, 'files')
   FILE_PATH: str = os.path.join(FILES_FOLDER, f'{code}_recipe_layer_number.tdms')

   open(FILE_PATH, 'wb').write(response.content)

   # Processing
   fill_database.fill_database_main(code=code)

   utils.clean_folder(FILES_FOLDER)
   
   return "201", 201
    


if __name__ == '__main__':
   app.run(
      debug=True,
      host='0.0.0.0',
      port=8003
   )
