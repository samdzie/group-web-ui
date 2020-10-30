FROM python:3.8
EXPOSE 5000
ENV FLASK_RUN_HOST="0.0.0.0"
WORKDIR /srv/group-web-ui
COPY server .
RUN ["pip", "install", "pipenv"]
RUN ["pipenv", "install", "--system", "--deploy", "--ignore-pipfile"]
CMD ["flask", "run"]
