# backend


Steps to build:
    Local:
        $ source setup_env.sh
        $ python app/py
    
    Docker:
        # check env variables in docker-compose.yaml; make sure the IPs is your docker-machine ip
        # check docker machine ip with "docker-machine ip"

        $ docker-compose build
        $ docker-compose up -d
        
        # do stuff

        $ docker-compose down
        