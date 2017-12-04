import requests
import time
import json
import sys
import traceback
from datetime import datetime

koinex_api_url = 'https://koinex.in/api/ticker'
time_delay_in_seconds = 10 * 60

# Utility functions
def print_last_traceback():
  printable_time =  datetime.utcfromtimestamp(time.time()).strftime("%d-%b-%Y, %H:%M:%S")
  print("\n\n------------- ERROR", printable_time, "----------------", file=sys.stderr, flush=True)
  traceback.print_exc(chain=False, limit=1)
  print('', file=sys.stderr, flush=True)

while(True):
  try:
    value_acquired = False    
    R = requests.get(koinex_api_url)
    R.raise_for_status()  # Raise an exception if response not 200
    R = R.content.decode('utf-8')  # Yes, I know I'm changing the type of variable
    btc_rate_in_inr = json.loads(R)['prices']['BTC']
    value_acquired = True  # wont execute if an exception occurs
  except requests.HTTPError:
    # This exception is mostly raised when you do too many API calls per second
    print_last_traceback()
  except json.decoder.JSONDecodeError:
    print_last_traceback()
    print("Could not parse the following response:\n" + R, file=sys.stderr, flush=True)
  except:
    print_last_traceback()
  finally:
    # Print the value ('missing' is printed if value was not acquired)
    time_now = time.time()
    if value_acquired:
      print(int(time_now), btc_rate_in_inr,
        datetime.utcfromtimestamp(time_now).strftime("%d-%b-%Y %H:%M:%S"),
        sep=",", flush=True
        )
    else:
        print(int(time_now), 'missing',
        datetime.utcfromtimestamp(time_now).strftime("%d-%b-%Y %H:%M:%S"),
        sep=",", flush=True
        )
    time.sleep(time_delay_in_seconds)