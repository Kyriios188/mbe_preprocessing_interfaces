import requests
from flask import Flask, request
from pathlib import Path
import os

import utils
from fill_database import fill_database
from export_database import export_database_main


app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start():

   code: str = request.args.get('code', type=str)
   
   SERVER_URL = f'http://127.0.0.1:8000'
   FILE_URL: str = f'/media/recipe_log/{code}_recipe.log'

   response = requests.get(SERVER_URL+FILE_URL)

   # End the process if the content is unreachable
   try:
      response.raise_for_status()
   except requests.exceptions.HTTPError:
      # If there was any error
      return str(response.status_code), response.status_code

   # The files folder is in the same folder as this file
   PARENT_FOLDER = Path(__file__).resolve().parent
   FILES_FOLDER: str = os.path.join(PARENT_FOLDER, 'files')
   FILE_PATH: str = os.path.join(FILES_FOLDER, f'{code}_recipe.log')

   open(FILE_PATH, 'wb').write(response.content)

   # Processing the file
   experiment_list = fill_database()

   # Sending the data to the SQL server
   export_database_main(experiment_list)

   utils.clean_folder(FILES_FOLDER)
   
   return "201", 201
    


if __name__ == '__main__':
   app.run(
      debug=True,
      host='0.0.0.0',
      port=8002
   )
