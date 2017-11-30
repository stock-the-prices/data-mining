# backend


Steps to build:
    Docker:
    ```
	# make sure DEPLOY_MODE is set to 'dev' or 'prod' in docker compose
        # check env variables in docker-compose.yaml; make sure the IPs is your docker-machine ip
        # check docker machine ip with "docker-machine ip"
        # can be found here http://<docker-machine-ip>:<port>/v1.0/ui/

        # in repo dir:

        $ source setup_env.sh
        $ docker-compose build
        $ docker-compose up -d

        # do stuff

        $ docker-compose down
    ```

For prod deploy:
    ```
    # can be found here `http://data-mining-se390.herokuapp.com/v1.0/ui/`

    $ source setup_env.sh
    $ heroku container:push web --app $APP_NAME
    ```
