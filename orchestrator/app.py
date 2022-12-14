import requests
from flask import Flask, request


app = Flask(__name__)

container_busy_status = {
   8002: False,
   8003: False,
   8004: False,
   8005: False  # TODO: divide status to show progress?
}

@app.route('/start', methods=['GET'])
def start():

   # If the containers are busy because of a previous request, send 503
   if all(not busy for busy in container_busy_status.values()):
      return "Server is busy, try again later", 503

   code: str = request.args.get('code', type=str)

   # Ask the containers to start the next process
   response1 = requests.get('http://127.0.0.1:8002/start', params={'code': code})
   response2 = requests.get('http://127.0.0.1:8003/start', params={'code': code})
   response3 = requests.get('http://127.0.0.1:8004/start', params={'code': code})
   response4 = requests.get('http://127.0.0.1:8005/start', params={'code': code})

   # The responses are NOT the result of their process, just an ACK
   # The process end is indicated by the end() function below 
   response_list = [response1, response2, response3, response4]
   if any(not r for r in response_list):
      return "ERROR", 500
   
   # Tell the frontend the request was accepted so it can save its form instance
   return "200", 200


@app.route('/end', methods=['GET'])
def end():
   """
   Called by data containers when they finished their task.

   """

   code: str = request.args.get('code', type=str)
   container: str = request.args.get('container', type=int)

   # Set the caller's status as idle
   container_busy_status[container] = True

   # If every data container is idle, tell the frontend so it can alert the user
   if all(not busy for busy in container_busy_status.values()):
      requests.get(f'http://127.0.0.1:8000/{code}/end')
   
   # Send OK to the container
   return "200", 200


if __name__ == '__main__':
   app.run(
      debug=True,
      host='0.0.0.0',
      port=8001
   )
