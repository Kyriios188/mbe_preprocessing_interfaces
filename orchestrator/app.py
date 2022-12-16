import requests
import os
from threading import Thread
import time
from flask import Flask, request


app = Flask(__name__)

ABS_TIME_CT, REL_TIME_CT, SENSOR_CT, SHUTTER_CT = 0, 1, 2, 3
CT_ADDR = {
   ABS_TIME_CT: 'http://127.0.0.1:8002/',
   REL_TIME_CT: 'http://127.0.0.1:8003/',
   SHUTTER_CT: 'http://127.0.0.1:8004/',
   SENSOR_CT: 'http://127.0.0.1:8005/',
}

def check_containers_reachable() -> bool:
   """
   Checks if all containers are reachable.
   
   """

   for addr in CT_ADDR.values():
      if not os.system("ping -c 1 -w2 " + addr + " > /dev/null 2>&1"):
         return False
   return True


def call_preprocessing_containers(code: str, start_time: float):

   response_dict = {}

   # Ask the containers to start the next process
   abs_time_ct_response = requests.get(CT_ADDR[ABS_TIME_CT]+'/start', params={'code': code})
   print(f"Received {abs_time_ct_response.status_code} from CT1 {time.time() - start_time}")
   response_dict[ABS_TIME_CT] = abs_time_ct_response.status_code

   if abs_time_ct_response.status_code == 201:
      pid = os.fork()

      if pid == 0:
         rel_time_ct_response = requests.get(CT_ADDR[REL_TIME_CT]+'/start', params={'code': code})
         print(f"Received {rel_time_ct_response.status_code} from CT2 {time.time() - start_time}")
         response_dict[REL_TIME_CT] = rel_time_ct_response.status_code

         if abs_time_ct_response.status_code == 201:
            sensor_ct_response = requests.get(CT_ADDR[SENSOR_CT]+'/start', params={'code': code})
            print(f"Received {sensor_ct_response.status_code} from CT4 {time.time() - start_time}")
            response_dict[SENSOR_CT] = sensor_ct_response.status_code

      else:

         shutter_ct_response = requests.get(CT_ADDR[SHUTTER_CT]+'/start', params={'code': code})
         print(f"Received {shutter_ct_response.status_code} from CT3 {time.time() - start_time}")
         response_dict[SHUTTER_CT] = shutter_ct_response.status_code


   if any((not r == 201) for r in response_dict.values()):
      requests.get(f'http://127.0.0.1:8000/end/{500}/')

   else:
      requests.get(f'http://127.0.0.1:8000/end/{201}/')


@app.route('/start', methods=['GET'])
def start():

   # TODO: replace prints with logs
   code: str = request.args.get('code', type=str)

   start_time = time.time()

   if check_containers_reachable():
      print('Reached all containers.')
      Thread(
         target=call_preprocessing_containers,
         kwargs={'code': code, 'start_time': start_time}
      ).start()

      # Tell the frontend the request was accepted so it can save its form instance
      return f"200 {time.time() - start_time}", 200

   else:
      return "Server error: one or more containers cannot be reached.", 500



if __name__ == '__main__':
   app.run(
      debug=True,
      host='0.0.0.0',
      port=8001
   )
