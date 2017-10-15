# recipe to build docker image for our app
FROM python:3.6

# create repo dir
RUN mkdir /data-mining
WORKDIR /data-mining

# copy all code to the repo dir
ADD . /data-mining/

# install dependencies
RUN pip install -r requirements.txt

EXPOSE 9090

# run app/start server
CMD ["python", "/data-mining/app.py"]
