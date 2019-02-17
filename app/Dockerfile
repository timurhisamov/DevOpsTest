FROM python:3.7.2-alpine3.9
ENV TZ=Europe/Moscow
WORKDIR /usr/src/app
RUN apk add bash
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD [ "python", "./service.py", "-conf", "./conf.yml" ]