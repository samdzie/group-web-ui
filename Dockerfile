FROM python:3.8
EXPOSE 5000
ENV FLASK_APP=server
ENV FLASK_RUN_HOST="0.0.0.0"
WORKDIR /srv/group-web-ui
COPY . .
RUN ["python", "-m", "pip", "install", "--upgrade", "pip"]
RUN ["pip", "install", "pipenv"]
RUN ["pipenv", "install", "--system", "--deploy", "--ignore-pipfile"]

# Yarn installation solution from here:
# https://stackoverflow.com/questions/46013544
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "yarn", "-y"]

RUN ["./scripts/build-for-server.sh"]
CMD ["flask", "run"]
