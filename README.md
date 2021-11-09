CallTrackingMetrics Python WebSockets
---------------------

Connect to CTM (CallTrackingMetrics) web socket service.  This allows you to connect your application into the status and realtime events available
in CallTrackingMetrics web interface and build this data into your own applications.

## Usage

```sh
python3 -m venv ctmsocketenv
pip3 install -r requirements.txt
```

From the CTM UI you'll need to get an API key and secret.  You can also connect using oauth2 - to do this you'll need an agency level account e.g. one of the 2 more advanced plans not the basic plan. 
Then you can navigate to https://app.calltrackingmetrics.com/oauth_apps and register your application to get a client key and secret.  We support two types of Oauth2, web based authentication and device flow for input constrained devices (think iot or tvs)

In the following example:
```
websocket-example.py
```

we'll use API keys.

# Environment for API Key Access

Export your basic authentication API keys from the account settings.  Keep in mind this example will only work with account level keys not agency level keys

```bash
export CTM_OKEN='a...d.....'
export CTM_SECRET='........'
export CTM_HOST='app.calltrackingmetrics.com'
export CTM_SOCKS='app.calltrackingmetrics.com'
```

Now you should be ready to run the websocket-example.py

```bash
python3 websocket-example.py
```

If you have python3 installed as python just run using python instead of python3...
