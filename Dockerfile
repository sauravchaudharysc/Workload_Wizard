FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3 python3-pip
# copy the flask app
    
WORKDIR /external-service

COPY ./external-service .


# final configuration and running the application with exposed port
# RUN gcc counter-service.c

RUN pip install flask==3.0.*
RUN pip install requests
RUN pip install psutil



ENV FLASK_APP=app.py
EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0"]