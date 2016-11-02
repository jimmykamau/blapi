[![Build Status](https://travis-ci.org/andela-jkamau/blapi.svg?branch=master)](https://travis-ci.org/andela-jkamau/blapi)   [![Coverage Status](https://coveralls.io/repos/github/andela-jkamau/blapi/badge.svg?branch=master)](https://coveralls.io/github/andela-jkamau/blapi?branch=master)  [![Codacy Badge](https://api.codacy.com/project/badge/Grade/ca89b1fb15a9449d831c5dad273ad60d)](https://www.codacy.com/app/jimmy-kamau/blapi?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-jkamau/blapi&amp;utm_campaign=Badge_Grade)

# blapi
A Flask API for a bucket list service


## Installation and setup
Clone this repo:
```
$ https://github.com/andela-jkamau/blapi.git
```


Navigate to the `blapi` directory:
```
$ cd blapi
```

Create a virtual environment and activate it using [this guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Install dependancies:
```
$ pip install -r requirements.txt
```

Initialize, migrate and update the database:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

Run tests to ensure everything is working as expected:
~~~
$ tox
GLOB sdist-make: /vagrant/2/setup.py
py34 inst-nodeps: /vagrant/2/.tox/dist/Blapi-1.0.0.zip
py34 installed: alembic==0.8.8,aniso8601==1.1.0,Blapi==1.0.0,blinker==1.4,click==6.6,coverage==4.2,coveralls==1.1,decorator==4.0.10,docopt==0.6.2,factory-boy==2.7.0,fake-factory==0.7.2,Faker==0.7.3,Flask==0.11.1,Flask-JWT==0.3.2,Flask-Mail==0.9.1,Flask-Migrate==2.0.0,Flask-Principal==0.4.0,Flask-RESTful==0.3.5,Flask-Script==2.0.5,Flask-SQLAlchemy==2.1,Flask-Testing==0.6.1,Flask-WTF==0.13,ipdb==0.10.1,ipython==5.1.0,ipython-genutils==0.1.0,itsdangerous==0.24,Jinja2==2.8,Mako==1.0.4,MarkupSafe==0.23,marshmallow==2.10.3,passlib==1.6.5,pexpect==4.2.1,pickleshare==0.7.4,pluggy==0.3.1,prompt-toolkit==1.0.8,psycopg2==2.6.2,ptyprocess==0.5.1,py==1.4.31,Pygments==2.1.3,PyJWT==1.4.2,python-dateutil==2.5.3,python-editor==1.0.1,pytz==2016.6.1,requests==2.11.1,simplegeneric==0.8.1,six==1.10.0,SQLAlchemy==1.0.15,tox==2.3.1,traitlets==4.3.1,virtualenv==15.0.3,wcwidth==0.1.7,Werkzeug==0.11.11,WTForms==2.1
py34 runtests: PYTHONHASHSEED='444480542'
py34 runtests: commands[0] | python -m unittest
.Authorization Required. Request does not contain an access token
..................
----------------------------------------------------------------------
Ran 19 tests in 1.479s

OK
_____________________________________________________________ summary ______________________________________________________________
  py34: commands succeeded
  congratulations :)
~~~


## Usage

Start the app by running
```
python manage.py runserver
```
~~~
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: xxx-xxx-xxx
~~~

Access the endpoints using your preferred client. You can use [Postman](https://www.getpostman.com/) for testing

### Endpoints

| Resource URL | Methods | Description | Requires Token |
| -------- | ------------- | --------- |--------------- |
| `/auth/register/` | POST  | User registration | FALSE |
| `auth/register/`  | GET | View all registered users | TRUE |
|  `/auth/login/` | POST | User login | FALSE |
| `/bucketlists/` | GET, POST | A user's bucket lists | TRUE |
| `/bucketlists/<bucketlist_id>` | GET, PUT, DELETE | A single bucket list | TRUE |
| `/bucketlists/<bucketlist_id>/items/` | GET, POST | Items in a bucket list | TRUE |
| `/bucketlists/<bucketlist_id>/items/<item_id>` | GET, PUT, DELETE | A single bucket list item | TRUE |

| Method | Description |
|------- | ----------- |
| GET | Retrieves a resource(s) |
| POST | Creates a new resource |
| PUT | Updates an existing resource |
| DELETE | Deletes an existing resource |
