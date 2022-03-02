import os
import sys
import re
import websocket
import http.client as httplib
import base64
import json
import urllib
import time
import requests
from requests.auth import HTTPBasicAuth

CTM_TOKEN      = os.environ['CTM_TOKEN']  # API key from account to connect a(account_id)d.....
CTM_PASS       = os.environ['CTM_SECRET'] # API sec from the account to connect
CTM_HOST       = os.environ['CTM_HOST']   # in production app.calltrackingmetrics.com
CTM_SOCKS      = os.environ['CTM_SOCKS']  # in production app.calltrackingmetrics.com

CTM_ACCOUNT_ID = re.search('a(\d+)d', CTM_TOKEN).group(1) # parse the account id from the api key
CTM_USER_ID    = None
CTM_CAPTOKEN   = None

def on_message(wsapp, message):
  print(message)
  if message == '42["access.handshake"]':
    output = json.dumps(["access.account", {"id": CTM_USER_ID, "account": CTM_ACCOUNT_ID, "captoken": CTM_CAPTOKEN}])
    r = wsapp.send("42" + output)
    print("sent access")

def on_close(wsapp, opt1, opt2):
  print ("Retry : %s" % time.ctime())

  # keep in mind this might not be the right way to keep the app running and could lead to too much recursion
  time.sleep(10)
  start_sockets()

def on_open(wsapp):
  print("on_open")
  wsapp.send("40")

def on_ping(wsapp, message):
  print("Got a ping! A pong reply has already been automatically sent.")

def on_pong(wsapp, message):
  print("Got a pong! No need to respond")
  wsapp.send("40")

def on_error(wsapp, error):
  print(f'{str(error)}   ### OFFLINE ###')

def start_sockets():
  socket_url = "wss://" + CTM_SOCKS + "/socket.io/?EIO=4&transport=websocket"
  print("connecting to: ", socket_url)

  wsapp = websocket.WebSocketApp(socket_url, on_open=on_open, on_close=on_close, on_message=on_message, on_ping=on_ping, on_pong=on_pong)
#  websocket.enableTrace(True)

  wsapp.run_forever(ping_interval=10, ping_timeout=5, ping_payload="40")

def get_user_id():
  res = requests.get("https://" + CTM_HOST + "/api/v1/accounts/" + CTM_ACCOUNT_ID + "/users", auth=HTTPBasicAuth(CTM_TOKEN, CTM_PASS))
  if res.status_code == 200:
    json = res.json()
    print(json["users"][0])
    return json["users"][0]["uid"]

def get_captoken():
  res = requests.post("https://" + CTM_HOST + "/api/v1/accounts/" + CTM_ACCOUNT_ID + "/users/captoken", auth=HTTPBasicAuth(CTM_TOKEN, CTM_PASS))
  if res.status_code == 200:
    txt = res.text

    json = eval(txt)
    return json['token']

CTM_USER_ID = get_user_id()
if CTM_USER_ID:
  print("got user_id: '%d'" % CTM_USER_ID)

CTM_CAPTOKEN = get_captoken()
if CTM_CAPTOKEN:
  print("got captoken: '%s'" % CTM_CAPTOKEN)

if CTM_CAPTOKEN and CTM_USER_ID:
  start_sockets()
