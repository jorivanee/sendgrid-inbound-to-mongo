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
14. `cp config.example.json config.json`
15. `nano config.json`

# Step 6 - Setting up uWSGI