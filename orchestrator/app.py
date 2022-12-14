import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start():

   code: str = request.args.get('code')

   response = requests.get('http://127.0.0.1:8002/start', params={'code': code})

   # THEN
   # Appel .csv container & .rel container
   # WHEN .rel container répond :
   # Appel tdms container
   

   return response.content


if __name__ == '__main__':
   app.run(
      debug=True,
      host='0.0.0.0',
      port=8001
   )
