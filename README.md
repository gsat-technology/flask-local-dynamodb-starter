Flask & Local DynamoDB starter kit
==================================

Note: requires [Docker Compose](https://docs.docker.com/compose/install/)

1. clone this repo
2. `cd flask-local-dynamodb-starter`
3. `pip install httpie`
4. Run docker compose `docker-compose up`
5. Initialise database by browsing to endpoint: `http://localhost:5000/tables/init`
6. Initialise database `cat user.json | http --json http://localhost:5000/user`
7. Confirm users have been created `http http://localhost:5000/user`

table action endpoints
----------------------
For convenience, these endpoints are available:

delete tables:
`http://localhost:5000/tables/delete`

list tables:
`http://localhost:5000/tables/list`

(re)initialise tables:
`http://localhost:5000/tables/init`


