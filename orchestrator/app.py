import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start():

    # Appel .log container

    # THEN
    # Appel .csv container & .rel container
    # WHEN .rel container répond :
    # Appel tdms container

    return str(request.args.get('code'))


if __name__ == '__main__':
   app.run(
      debug=True,
      host='0.0.0.0',
      port=8001
   )
