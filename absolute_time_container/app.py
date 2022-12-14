import requests
from flask import Flask, request
from pathlib import Path
import os

app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start():

   code: str = str(request.args.get('code'))
   
   SERVER_URL = f'http://127.0.0.1:8000'
   FILE_URL: str = f'/media/recipe_log/{code}_recipe.log'

   response = requests.get(SERVER_URL+FILE_URL)

   # The files folder is in the same folder as this file
   parent_folder = Path(__file__).resolve().parent
   file_path: str = os.path.join(parent_folder, 'files', f'{code}_recipe.log')

   open(file_path, 'wb').write(response.content)

   # Processing
   
   return "", response.status_code
    


if __name__ == '__main__':
   app.run(
      debug=True,
      host='0.0.0.0',
      port=8002
   )
