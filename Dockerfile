FROM simpleservices/python3

COPY . /opt/project
WORKDIR /opt/project

RUN pip install -r requirements.txt

ENV FLASK_APP=server.py 
EXPOSE 5000

ENTRYPOINT python3 -m flask run --host=0.0.0.0
    
