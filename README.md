<<<<<<< HEAD
# Weather Prediction System
A website that uses machine learning to predict the weather.

## What it looks like:
![prediction example](./.github/prediction.png?raw=true)

## Features
- Flask web server for Debian/Ubuntu
- Login and signup page
- Cookie usage when user logs in
- Database for user login credentials
- Password hashing
- Random Forest Classifier model that takes user's inputs and predicts weather

## Setup Development Server
To create a quick-and-dirty server, follow these instructions:
1. Install Python and pip
4. pip install -r requirements.txt
5. Run the shell script
6. Go to 127.0.0.1:5000 for localhost or the private IP address of the server in a browser

## Setup Production Server
To create a server the proper way, follow these instructions:
1. Install Python 3.10.4, pip, and venv. Pyenv is preferred for this.
2. `apt install nginx git`
3. `git clone https://github.com/WillChamness/WeatherPredictionSystem && cd WeatherPredictionSystem`
4. `python -m venv env` and `source env/bin/activate`
5. Install `gunicorn` with pip or apt. Pip is preferred and will be assumed for the gunicorn config.
6. `pip install -r requirements.txt`
7. Change the last line in `app.py` to `app.run(host='0.0.0.0', debug=False)`
8. Use the Nginx configuration below
9. Use the gunicorn daemon configuration below
10. Go to the IP address of the server in a browser


### Nginx Config
Create `/etc/nginx/sites-enabled/flask-app` and add the following:
```
server {
        listen 80 default_server;

        location / {
                proxy_pass http://127.0.0.1:8000; # port number not a typo
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
```
Then unlink the default config and test the syntax:
```
sudo unlink /etc/nginx/sites-enabled/default
sudo nginx -t
```
If there are no errors, reload Nginx: 
```
sudo nginx -s reload
```

### Gunicorn Config
Create `/etc/systemd/system/weather-prediction.service` and add the following:
```
[Unit]
Description=Flask App

[Service]
Type=simple
ExecStart=/path/to/WeatherPredictionSystem/env/bin/gunicorn --chdir /path/to/WeatherPredictionSystem/ app:app

[Install]
WantedBy=multi-user.target
```

Then start and check the service:
```
sudo systemctl start weather-prediction
sudo systemctl status weather-prediction
```

If there are no errors, enable the service:
```
sudo systemctl enable weather-prediction
```
=======
# -Python
Это совместный проект с Баландиной Марией
>>>>>>> aa8926b1b50f86cc952573dd260391b46faf65f5
