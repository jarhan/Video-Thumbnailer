from flask import Flask, render_template, request, redirect
import requests
import logging

WEB_URL = "http://localhost:34782/"
SOS_BASE_URL = 'http://simple-object-storage:8080'
MAKE_THUMBNAIL = 'http://milestone2_queue-wrapper_1:5000'

LOG = logging
LOG.basicConfig(
    level=LOG.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

@app.route('/')
def student():
    return render_template('home.html')

@app.route('/delete/<bucket_name>',methods = ['DELETE', 'GET'])
def delete_thumbnail_all(bucket_name):
    try:
        r = requests.get(MAKE_THUMBNAIL + '/' + bucket_name + '?list')
        resp = r.json()
        objects = resp['gif']

        for obj in objects:
            delete_thumbnail(bucket_name, obj['name'])
        return redirect(WEB_URL + bucket_name + "/show_all_gifs")
    except:
        return render_template("error_page.html")

@app.route('/delete/<bucket_name>/<object_name>',methods = ['DELETE', 'GET'])
def delete_thumbnail(bucket_name, object_name):
    LOG.info('delete')
    try:
        r = requests.delete(SOS_BASE_URL + '/' + bucket_name + '/' + object_name + '?delete')
        LOG.info(r.content)
        return redirect(WEB_URL + bucket_name + "/show_all_gifs")
    except Exception as e:
        return render_template("error_page.html")

@app.route('/make-thumbnail/<bucket_name>',methods = ['POST', 'GET'])
def make_thumbnail_all(bucket_name):
    try:
        r = requests.get(SOS_BASE_URL + '/' + bucket_name + '?list')
        resp = r.json()
        objects = resp['objects']

        for obj in objects:
            make_thumbnail(bucket_name, obj['name'])
        return redirect(WEB_URL + bucket_name + "/show_all_gifs")
    except:
        return render_template("error_page.html")

@app.route('/make-thumbnail/<bucket_name>/<object_name>',methods = ['POST', 'GET'])
def make_thumbnail(bucket_name, object_name):
    LOG.info('make_thumbnail')
    try:
        r = requests.post(MAKE_THUMBNAIL + '/make-thumbnail', json={"bucket": bucket_name, "object": object_name})
        LOG.info(r.content)
        return redirect(WEB_URL + bucket_name + "/show_all_gifs")
    except Exception as e:
        return render_template("error_page.html")

@app.route('/<bucket_name>/show_all_<object>s', methods=['POST', 'GET'])
def show_all(bucket_name, object):
    collector = []
    if (object == 'video'):
        BASE_URL = SOS_BASE_URL
        key = 'objects'
        html_file = 'bucket_videos.html'
    elif (object == 'gif'):
        BASE_URL = MAKE_THUMBNAIL
        key = 'gif'
        html_file = 'bucket_gifs.html'
    else:
        html_file = 'error_page.html'
    try:
        r = requests.get(BASE_URL + '/' + bucket_name + '?list')
        resp = r.json()
        objects = resp[key]

        for obj in objects:
            object_name = obj['name']
            collector.append(object_name)

    except Exception as e:
        bucket_name = bucket_name + " does not exist"

    return render_template(html_file, bucket_name = bucket_name, objects = collector)
if __name__ == '__main__':
    app.run(debug = True, port=33467)
