Webpage for my engineer's thesis.  On Raspberry PI there are sensors, that measure temperature, humidity, ashes etc.  Measurements are sent to the webpage and then processed. 
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

TODO!!!


Testing
============

TODO!!!