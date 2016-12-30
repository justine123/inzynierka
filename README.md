Webpage for my engineer's thesis.  On Raspberry PI there are sensors, that measure temperature, humidity, dust level etc.  Measurements are sent to the webpage and then processed. 
==============================================================================================================================================================================

Installation
============

On your system install: 

* Python 2.7
* pip
* virtualenv and virtualenvwrapper:
```
pip install virtualenv
pip install virtualenvwrapper
```
* configure virtualenv (documentation: http://docs.python-guide.org/en/latest/dev/virtualenvs/)
* create new virtualenv: 
```mkvirtualenv inzynierka```
* configure postactivate file: 
```
echo "export DJANGO_SETTINGS_MODULE=inzynierka.settings" >> ~/.virtualenvs/inzynierka/bin/postactivate
echo "cd $(pwd)" >> ~/.virtualenvs/inzynierka/bin/postactivate 
```
* install requirements: 
```pip install -r doc/requirements.txt```
* restart virtualenv:
```
deactivate
workon inzynierka
```
* runserver:
```./manage.py runserver```
* run tasks in the background (in another terminal tab):
```
python manage.py process_tasks
```
* open new tab in your web browser and go to address: http://127.0.0.1:8000/


Using the app
============

On the main page there is a map of all the sensors. 

After logging in on a sensor, user can see its data presented with charts.

On the time chart page, user can choose which weather conditions he wants to observe and a time frame (day/ week/ all the time). After submitting the form, proper chart is rendered with chosen categories and time period.

On the correlation chart page, user can choose which weather conditions he wants to correlate - one for x-axis and one or more for y-axis. After submitting the form, proper chart is rendered with chosen x and y axis.
