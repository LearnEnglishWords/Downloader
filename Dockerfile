FROM simpleservices/python3

COPY . /opt/project
WORKDIR /opt/project

RUN pip3 install -r requirements.txt
RUN bash -c "mkdir -p static/sounds/{words,examples} && mkdir -p static/words"

ENV FLASK_APP=server.py 
EXPOSE 5000

ENTRYPOINT python3 -m flask run --host=0.0.0.0
    
