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
        if not body:
            raise Exception('Missing Json Body')
        if 'bucket' not in body:
            raise Exception('Missing Bucket name')
        if 'target_bucket' not in body:
            body['target_bucket'] = body['bucket']
        if 'object' not in body:
            loop_push_in_queue(body)
        else: # contain both bucket_name and object_name
            # if 'target_object' not in body:
            #     body['target_object'] = body['object'] + ".gif"
            # else:
            #     target_object_name = body['target_object']
            #     if not target_object_name.endswith(".gif"):
            #         body['target_object'] = target_object_name + ".gif"
            new_body = check_target_object_name(body)
            LOG.info(new_body)
            push_in_queue(new_body)
        return jsonify({'status': 'OK'})
    except Exception as ex:
        return jsonify({'status': 'BAD REQUEST', 'error description': ex.args}), 400

def check_target_object_name(body):
    if 'target_object' not in body:
        body['target_object'] = body['object'] + ".gif"
    else:
        target_object_name = body['target_object']
        if not target_object_name.endswith(".gif"):
            body['target_object'] = target_object_name + ".gif"
    return body

def loop_push_in_queue(body):
    bucket_name = body['bucket']
    objects = list_objects_in_bucket(bucket_name)
    if not objects:
        raise Exception('No Object in Bucket')
    for obj in objects:
        object_name = obj['name']
        body['object'] = object_name
        body['target_object'] = object_name + ".gif"
        LOG.info(body)
        push_in_queue(body)

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
