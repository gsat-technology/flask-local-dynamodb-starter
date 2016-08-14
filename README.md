Flask & Local DynamoDB starter kit
----------------------------

Note: requires [Docker Compose](https://docs.docker.com/compose/install/)

1. clone this repo
2. `cd flask-local-dynamodb-starter`
3. `pip install httpie`
4. Run docker compose `docker-compose up`
3. Initialise database `cat user.json | http --json http://localhost:5000/user`


