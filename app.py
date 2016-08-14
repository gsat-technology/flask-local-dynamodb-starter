import json
import uuid
from pprint import pprint

import boto3
from flask import request
from flask import Flask
from nocache import nocache

app = Flask(__name__)
flask_client = app.test_client()


dynamodb_endpoint='http://dynamodb:8000'
ddb_client = boto3.client('dynamodb',
                      aws_access_key_id="anything",
                      aws_secret_access_key="anything",
                      endpoint_url=dynamodb_endpoint,
                      region_name='ap-southeast-2')

ddb_resource = boto3.resource('dynamodb',
                      aws_access_key_id="anything",
                      aws_secret_access_key="anything",
                      endpoint_url=dynamodb_endpoint,
                      region_name='ap-southeast-2')


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/user', methods=['GET', 'POST'])
@nocache
def user_create():
    print 'flask: user_create()'

    if request.method == 'GET':
        user_table = ddb_resource.Table('user')
        result = user_table.scan()
        return json.dumps(result['Items'])
    else:

        body_json = request.get_json()

        for user in body_json['users']:
            user['id'] = str(uuid.uuid4())[:6]
            user_table = ddb_resource.Table('user')
            user_table.put_item(Item=user)        

            response = user_table.get_item(Key={'id': user['id']})
            pprint(response)

        return 'created'



@app.route('/tables/delete')
@nocache
def tables_delete():
    print 'flask: tables_delete()' 
    
    tables = json.loads(flask_client.get('/tables/list').data)

    for table in tables:
        response = ddb_client.delete_table(TableName=table)
        print response

    return 'deleted'


@app.route('/tables/list')
@nocache
def tables_list():
    print 'flask:tables_list()'

    response = ddb_client.list_tables()
    print response
    return json.dumps(response['TableNames'])


@app.route('/tables/init')
@nocache
def tables_init():
    print 'flask:tables_init()'

    flask_client.get('/tables/delete')

    table = ddb_client.create_table(
      TableName='user',
      KeySchema=[
        {
          'AttributeName': 'id',
          'KeyType': 'HASH' 
        }
      ],
      AttributeDefinitions=[
        {
          'AttributeName': 'id',
          'AttributeType': 'S'
        },
      ],
      ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
      }
    )

    if table['TableDescription']['TableStatus'] == 'ACTIVE':
        return 'okay'
    else:
        return 'error creating dyanamo_db table'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
