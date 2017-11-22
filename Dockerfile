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

# ENV Variables

# assigned default
# ENV PORT 9090

ENV MONGODB_HOST localhost
ENV MONGODB_PORT 27017

ENV NEWS_API_KEY e7e67041d3604b098c2668f349a1fadd

# run app/start server
CMD ["python", "/data-mining/app.py"]

