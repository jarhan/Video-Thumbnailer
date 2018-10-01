#!/usr/bin/env python3
import os
import logging
import json
import uuid
import redis
import requests
import subprocess

LOG = logging
REDIS_QUEUE_LOCATION = os.getenv('REDIS_QUEUE', 'localhost')
# SOS_ENV = os.getenv('SOS_HOST', 'localhost')
QUEUE_NAME = 'queue:factoring'
SOS_BASE_URL = 'http://sos:8080'
# SOS_BASE_URL = f"http://{SOS_ENV}:8080"

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
                # task = json.loads(packed_task)
                task = json.loads(packed_task.decode('utf8').replace("'", '"'))
            except Exception:
                LOG.exception('json.loads failed')
            if task:
                callback_func(task)

def download_object(bucket_name, object_name):
    try:
        # os.path.exists(path)
        file_path = "./resources/video/"+bucket_name+"/"+object_name

        # my_file = Path(file_path)
        if (not os.path.exists(file_path)):
            os.mkdir("./resources/video/"+bucket_name)
            r = requests.get(SOS_BASE_URL + '/' + bucket_name + '/' + object_name)

            response = r.content

            f= open("./resources/video/"+bucket_name+"/"+object_name,"wb")
            f.write(response)
    except Exception:
        raise Exception('Download failed')

def make_thumbnail(bucket_name, object_name, target_bucket_name, target_object_name):
    try:
        video_name = bucket_name+"/"+object_name
        gif_name = video_name+".gif"
        subprocess.run(["./make_thumbnail.sh", video_name, gif_name, target_bucket_name, target_object_name])
    except Exception:
        raise Exception('Make .gif failed')

def execute_factor(log, task):
    bucket_name = task.get('bucket')
    object_name = task.get('object')

    target_bucket_name = bucket_name
    target_object_name = object_name

    log.info(bucket_name)

    if bucket_name:
        log.info('Bucket name: %s', bucket_name)

        if object_name:
            log.info('Object name: %s', object_name)
            log.info('Download each file')

            download_object(bucket_name, object_name)
            make_thumbnail(bucket_name, object_name, target_bucket_name, target_object_name)

        else:
            log.info('No Object name given')
            log.info(requests.get(SOS_BASE_URL + '/' + bucket_name + '?list').content)
            log.info('Download all objects in bucket')
    else:
        log.info('No Bucket name given')
        log.info('Cannot download')

    # subprocess.run(["docker run", "-v $(pwd)/resources:/resources" "video_thumnailer" "make_thumbnail" "vatanika.mp4" "output.gif"])
    # subprocess.run(["./make_thumbnail.sh", "vatanika.mp4", "o4.gif"])
    # subprocess.run(["pwd"])
    # subprocess.run(["ls", "-la"])
    # subprocess.run(["ls", "resources/gif"])
    #
    # print('in get_sos_list')
    # log.info(requests.get('http://sos:8080/all').content)


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
        lambda task_descr: execute_factor(named_logging, task_descr))

if __name__ == '__main__':
    main()
