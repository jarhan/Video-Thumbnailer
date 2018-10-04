#!/usr/bin/env python3
import os
import logging
import json
import uuid
import redis
import requests
import subprocess
import hashlib

LOG = logging
REDIS_QUEUE_LOCATION = os.getenv('REDIS_QUEUE', 'localhost')

QUEUE_NAME = 'queue:factoring'
SOS_BASE_URL = 'http://simple-object-storage:8080'

INSTANCE_NAME = uuid.uuid4().hex

LOG.basicConfig(
    level=LOG.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def watch_queue(redis_conn, queue_name, callback_func, timeout=30):
    active = True

    while active:
        # Fetch a json-encoded task using a blocking (left) pop
        packed = redis_conn.blpop([queue_name], timeout=timeout)

        if not packed:
            # if nothing is returned, poll a again
            continue

        _, packed_task = packed

        # If it's treated to a poison pill, quit the loop
        if packed_task == b'DIE':
            active = False
        else:
            task = None
            try:
                task = json.loads(packed_task.decode('utf8').replace("'", '"'))
            except Exception:
                LOG.exception('json.loads failed')
            if task:
                callback_func(task)

def download_object(bucket_name, object_name):
    LOG.info("in download_object")
    LOG.info(bucket_name)
    LOG.info(object_name)
    try:
        worker_path = "./resources/video/"+INSTANCE_NAME
        bucket_path = worker_path+"/"+bucket_name
        object_path = bucket_path+"/"+object_name

        LOG.info(worker_path)
        LOG.info(bucket_path)
        LOG.info(object_path)

        if (not os.path.exists(worker_path)):
            os.mkdir(worker_path)
        if (not os.path.exists(bucket_path)):
            os.mkdir(bucket_path)
        if (not os.path.exists(object_path)):
            r = requests.get(SOS_BASE_URL + '/' + bucket_name + '/' + object_name)

            response = r.content
            LOG.info(r.status_code)
            if (r.status_code != 200):
                raise Exception('Download failed')
            f= open("./resources/video/"+INSTANCE_NAME+"/"+bucket_name+"/"+object_name,"wb")
            f.write(response)
    except Exception:
        raise Exception('Download failed')

def make_thumbnail(bucket_name, object_name):
    LOG.info("in make_thumbnail")
    LOG.info(bucket_name)
    LOG.info(object_name)
    try:
        subprocess.run(["./make_thumbnail.sh",INSTANCE_NAME, bucket_name, object_name])
    except Exception:
        raise Exception('Make .gif failed')

def upload_gif(bucket_name, object_name, target_bucket_name, target_object_name):
    create_bucket_r = requests.post(SOS_BASE_URL + '/' + target_bucket_name + '?create')
    create_bucket_response_status = create_bucket_r.status_code
    if (create_bucket_response_status != 200 and create_bucket_response_status != 400):
        raise Exception("Cannot create bucket")

    create_object_r = requests.post(SOS_BASE_URL + '/' + target_bucket_name + '/' + target_object_name + '?create')
    create_object_response_status = create_object_r.status_code
    if (create_object_response_status != 200):
        raise Exception("Cannot create object")

    gif_file_path = './resources/gif/' + INSTANCE_NAME + '/' + bucket_name + '/' + object_name + '.gif'
    upload_url = SOS_BASE_URL + '/' + target_bucket_name + '/' + target_object_name + '?partNumber=1'
    data = open(gif_file_path, 'rb').read()

    upload_object_r = requests.put(url=upload_url, data=data, headers={ 'Content-MD5': hashlib.md5(data).hexdigest()})
    upload_object_response_status = upload_object_r.status_code
    if (upload_object_response_status != 200):
        if (upload_object_response_status == 400):
            error_description = 'Error from upload'
            # error_description = upload_object_response['error']
            raise Exception(error_description)
        else: raise Exception("Cannot upload object")

    complete_object_r = requests.post(SOS_BASE_URL + '/' + target_bucket_name + '/' + target_object_name + '?complete')
    complete_object_response_status = complete_object_r.status_code
    if (complete_object_response_status != 200):
        raise Exception("Cannot complete object")

def execute(log, task):
    try:
        bucket_name = task.get('bucket')
        object_name = task.get('object')
        target_bucket_name = task.get('target_bucket')
        target_object_name = task.get('target_object')

        log.info("in execute")
        log.info(task)

        download_object(bucket_name, object_name)
        make_thumbnail(bucket_name, object_name)
        upload_gif(bucket_name, object_name, target_bucket_name, target_object_name)

        log.info("done")
    except Exception as ex:
        log.info("except in execute")
        log.info(ex.args)

def main():
    LOG.info('Starting a worker...')
    LOG.info('Unique name: %s', INSTANCE_NAME)
    host, *port_info = REDIS_QUEUE_LOCATION.split(':')
    port = tuple()
    if port_info:
        port, *_ = port_info
        port = (int(port),)

    named_logging = LOG.getLogger(name=INSTANCE_NAME)
    named_logging.info('Trying to connect to %s [%s]', host, REDIS_QUEUE_LOCATION)
    redis_conn = redis.Redis(host=host, *port)
    watch_queue(
        redis_conn,
        QUEUE_NAME,
        lambda task_descr: execute(named_logging, task_descr))

if __name__ == '__main__':
    main()
