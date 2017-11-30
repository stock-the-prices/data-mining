# backend

Deployed in Docker containers.

Local build:
* make sure DEPLOY_MODE is set to 'dev' in `docker-compose.yaml`
* check env variables in `docker-compose.yaml`; make sure the IPs is your docker-machine ip
* local can be found here `http://<docker-machine-ip>:<port>/v1.0/ui/`

```
$ source setup_env.sh
$ docker-compose build
$ docker-compose up -d

do stuff...

$ docker-compose down
```

Prod
* make sure DEPLOY_MODE is set to 'prod' in `docker-compose.yaml`
* host at `http://data-mining-se390.herokuapp.com/v1.0/ui/`

```
$ source setup_env.sh
$ heroku container:push web --app $APP_NAME
```
