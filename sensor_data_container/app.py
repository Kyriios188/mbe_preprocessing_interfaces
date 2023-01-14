from pathlib import Path
import os
import requests

from flask import Flask, request

import utils
import fill_database


app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start():

   code: str = request.args.get('code', type=str)
   
   SERVER_URL = f'http://127.0.0.1:8000'

   FILE_URLS: dict[str, str] = {
      f'/media/reflectivity_tdms/{code}_reflectivity.tdms': f'{code}_reflectivity.tdms',
      f'/media/roughness_tdms/{code}_roughness.tdms': f'{code}_roughness.tdms',
      f'/media/curvature_tdms/{code}_curvature.tdms': f'{code}_curvature.tdms',
      f'/media/wafer_temperature_tdms/{code}_wafer_temperature.tdms': f'{code}_wafer_temperature.tdms'
   }

   # The files folder is in the same folder as this file
   PARENT_FOLDER = Path(__file__).resolve().parent
   FILES_FOLDER: str = os.path.join(PARENT_FOLDER, 'files')


   for file_path_map in FILE_URLS.items():
      response = requests.get(SERVER_URL+file_path_map[0])
      file_path = os.path.join(FILES_FOLDER, file_path_map[1])

      open(file_path, 'wb').write(response.content)

   # Processing
   fill_database.tdms_extraction_main(code=code)
   

   utils.clean_folder(FILES_FOLDER)
   
   return "201", 201
   


if __name__ == '__main__':
   app.run(
      debug=True,
      host='0.0.0.0',
      port=8004
   )
