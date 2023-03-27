# sendgrid-inbound-to-mongo
Small web server to send all messages from a Sendgrid inbound parse webhook to a MongoDB database


# Installation:

# Step 1 - Installing the Python components
1. `sudo apt update`
2. `sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools`
   
# Step 2 - Installing MongoDB as a service
3. `wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -`
4. `echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list`
5. `sudo apt update`
6. `sudo apt install mongodb-org`
7. `sudo systemctl start mongod`
8. `sudo systemctl enable mongod`
# Step 3 - Cloning the repository
9. `git clone https://github.com/jorivanee/sendgrid-inbound-to-mongo webhook && cd webhook`

# Step 4 - Setting up the Python Virtual Environment
10. `sudo apt install python3-venv`
11. `python3 -m venv prod`
12. `source prod/bin/activate`

# Step 5 - Setting up the Flask Application
13. `pip install -r requirements.txt`
14. `deactivate`
15. `cp config.example.json config.json`
16. `sudo nano config.json`

# Step 6 - Setting up uWSGI
16. `sudo nano /etc/systemd/system/application.service`
17. Add the following lines:
>[Unit]
>Description=uWSGI instance to serve Webhook
>After=network.target
>
>[Service]
>User=<your username>
>Group=www-data
>WorkingDirectory=/home/<your username>/webhook
>Environment="PATH=/home/<your username>/webhook/prod/bin"
>ExecStart=/home/<your username>/webhook/prod/bin/uwsgi --ini application.ini
>
>[Install]
>WantedBy=multi-user.target
18. `sudo systemctl start application`
19. `sudo systemctl enable application`

# Step 7 - Setting up NGINX
20. `sudo apt install nginx`
21. `sudo nano /etc/nginx/sites-available/webhook`
22. Add the following lines:
>server {
>    listen 80;
>
>    location / {
>        include uwsgi_params;
>        uwsgi_pass unix:/home/<your username>/webhook/application.sock;
>    }
>}
23. `sudo ln /etc/nginx/sites-available/webhook /etc/nginx/sites-enabled/webhook