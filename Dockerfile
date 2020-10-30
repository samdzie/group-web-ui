FROM python:3.8
EXPOSE 5000
ENV FLASK_APP=server
ENV FLASK_RUN_HOST="0.0.0.0"
WORKDIR /srv/group-web-ui
COPY . .
RUN ["python", "-m", "pip", "install", "--upgrade", "pip"]
RUN ["pip", "install", "pipenv"]
RUN ["pipenv", "install", "--system", "--deploy", "--ignore-pipfile"]
RUN ["./scripts/build-for-server.sh"]
CMD ["flask", "run"]
