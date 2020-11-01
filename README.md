# Local setup:
```
virtualenv -p python3 venv
source ./lew-dev/bin/activate
mkdir static
pip install -r requirements.txt
```

run server:
```
FLASK_APP=server.py python3 -m flask run --host=0.0.0.0
```

run with docker:
```
docker-compose build
docker-compose up
```

# Special thanks:

 - [Flask](http://flask.pocoo.org/): Python microframework.



# Authors:

 - Martin Jablečník

