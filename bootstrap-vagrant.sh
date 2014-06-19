#!/usr/bin/env bash
sudo apt-get update

# Install dependencies
sudo apt-get -y install make libpq-dev git libsqlite3-dev g++

# Install Node.js (used by grunt to build statics)
# wget http://nodejs.org/dist/v0.10.29/node-v0.10.29.tar.gz # This gives us NPM v1.3.24 instead of v1.4.*
wget http://nodejs.org/dist/v0.10.24/node-v0.10.24.tar.gz
tar -xvf node-*
cd node-*
#/usr/bin/python2.7 configure
./configure
make
sudo make install
cd -
# We want some information when npm is running.
sudo npm config set loglevel info --global

# Install python
wget https://www.python.org/ftp/python/3.4.0/Python-3.4.0.tar.xz
tar -xvf Python-*.tar.xz
cd Python-*
./configure
make
sudo make install
# Link the new binary to python
sudo unlink /usr/bin/python
sudo ln -s /usr/local/bin/python3.4 /usr/local/bin/python
#sudo ln -s /usr/local/bin/pip3 /usr/local/bin/pip
cd -

# Install pip
wget http://python-distribute.org/distribute_setup.py
sudo python distribute_setup.py
sudo easy_install pip

# Install django - This might actually be included in the requirements.txt
# sudo pip install Django

# Install app requirements
cd /vagrant
sudo pip install -r requirements.txt

#  the database ready
python manage.py syncdb
# Run migrations
python manage.py migrate

# Remove any existing modules
rm -rf node_modules
# Installing dependencies.
npm install
# Build static files
sudo npm install grunt-cli -g

# Build it all
grunt

# python manage.py fasts3collectstatic --settings=global_change_lab.settings_s3