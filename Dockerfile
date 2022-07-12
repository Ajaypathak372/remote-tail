FROM python:3.9.13-slim-buster

WORKDIR /client

COPY client/* ./

#ENTRYPOINT [ "python", "client.py"]

CMD [ "./run.sh" ]