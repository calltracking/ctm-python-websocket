# python3 % <user_id> <account_id> '<cap token>'
import sys
import socketio

if len(sys.argv) < 3:
  print("python3 foo.py <user_id> <account_id> '<captoken>'")
  exit
user_id    = sys.argv[1]
account_id = sys.argv[2]
cap_token  = sys.argv[3]

print("using user: %s, account: %s  and cap token: %s\n" % (user_id, account_id, cap_token))


sio = socketio.Client(logger=True, engineio_logger=True)

@sio.event
def connect():
  print("I'm connected!")
  sio.emit('access.account', {'id': user_id, 'account': account_id, 'captoken': cap_token})
  print('sent access request')

@sio.on("auth.granted")
def on_auth_granted(data):
  print("auth granted", data)

@sio.on("auth.denied")
def on_auth_denied():
  print("auth denied!")

@sio.event
def connect_error(data):
  print("The connection failed!")

@sio.event
def disconnect():
  print("I'm disconnected!")

@sio.event
def my_message(data):
  print('message received with ', data)
  sio.emit('my response', {'response': 'my response'})

sio.connect('https://app.calltrackingmetrics.com', transports=['websocket'])
sio.wait()
