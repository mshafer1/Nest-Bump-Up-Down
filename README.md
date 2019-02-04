# Nest-Bump-Up-Down
A utility for controlling a nest thermostat via the Python API allowing for shifting the target temperature from the current temperate as desired.

## Requirements
This tool is build on top of the Nest Python API:

* [python-nest](https://github.com/nestlabs/nest-python)
* Nest API Key: details at [python-nest repo](https://github.com/nestlabs/nest-python) and [developers.nest.com](https://developers.nest.com/guides/get-started)

## Installation

* ```
git clone https://github.com/mshafer1/Nest-Bump-Up-Down.git
cd Nest-Bump-Up-Down
python3 setup.py install
```
* Edit `config.py` as desired (put in API key and client secret at minimum)


## Use with Web Server

### Apache2

* Enable CGI mode
* place hot.py, cold.py, and fan.py where accessible by server

Instructions at: [How To Set Up LAMP Server Without Frameworks](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-apache-mysql-and-python-lamp-server-without-frameworks-on-ubuntu-14-04)

### NGinX

* See example for [Raspberry Pi](http://raspberrywebserver.com/cgiscripting/setting-up-nginx-and-uwsgi-for-cgi-scripting.html)