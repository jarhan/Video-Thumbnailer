import os
import json
import logging
import redis
import requests
from flask import Flask, jsonify, request

LOG = logging
LOG.basicConfig(
    level=LOG.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
SOS_BASE_URL = 'http://sos:8080'

app = Flask(__name__)

class RedisResource:
    REDIS_QUEUE_LOCATION = os.getenv('REDIS_QUEUE', 'localhost')
    QUEUE_NAME = 'queue:factoring'

    host, *port_info = REDIS_QUEUE_LOCATION.split(':')
    port = tuple()
    if port_info:
        port, *_ = port_info
        port = (int(port),)

    conn = redis.Redis(host=host, *port)

@app.route('/factor', methods=['POST'])
def post_factor_job():
    body = request.json
    json_packed = json.dumps(body)
    print('packed:', json_packed)
    RedisResource.conn.rpush(
        RedisResource.QUEUE_NAME,
        json_packed)

    return jsonify({'status': 'OK'})

@app.route('/list-sos', methods=['GET'])
def get_sos_list():
    body = request.json
    json_packed = json.dumps(body)
    print('packed:', json_packed)
    RedisResource.conn.rpush(
        RedisResource.QUEUE_NAME,
        json_packed)

    return jsonify({'status': 'OK'})

@app.route('/make-thumbnail', methods=['POST'])
def make_thumbnail():
    try:
        body = request.json
        if 'bucket' not in body:
            raise Exception('Missing Bucket name')
        if 'object' not in body:
            loop_push_in_queue(body)
        else: # contain both bucket_name and object_name
            LOG.info(body)
            # push_in_queue(body)
        return jsonify({'status': 'OK'})
    except Exception as ex:
        return jsonify({'status': 'BAD REQUEST', 'error description': ex.args})

def loop_push_in_queue(body):
    bucket_name = body['bucket']
    objects = list_objects_in_bucket(bucket_name)
    if not objects:
        raise Exception('No Object in Bucket')
    for obj in objects:
        object_name = obj['name']
        LOG.info(object_name)
        tmp_body = jsonify({'bucket': bucket_name, 'object': object_name})
        LOG.info(tmp_body.json)
        # push_in_queue(tmp_body)

def list_objects_in_bucket(bucket_name):
    r = requests.get(SOS_BASE_URL + '/' + bucket_name + '?list')
    resp = r.json()
    return resp['objects']

def push_in_queue(body):
    LOG.info("in push_in_queue")
    json_packed = json.dumps(body)
    print('packed:', json_packed)
    RedisResource.conn.rpush(
        RedisResource.QUEUE_NAME,
        json_packed)
