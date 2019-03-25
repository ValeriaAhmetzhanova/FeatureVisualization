import os
os.environ['CUDA_VISIBLE_DEVICES']='0'

import flask

from flask import Flask
from flask import jsonify
from flask import send_file

from flask_cors import CORS

from database import db_session
from models import Job, Visualization, VisualizationResult, STATUS_MAP

from lucid.modelzoo import vision_models
from lucid.modelzoo.nets_factory import get_model

from network_utils import NETWORK_DESCRIPTION

# from processor import ProcessorThread
# import atexit


# def close_running_threads():
#     print('joining threads')
#     processor_thread.stop()
#     processor_thread.join()

# atexit.register(close_running_threads)

app = Flask(__name__)
CORS(app)


api_version = 'v1'

# processor_thread = ProcessorThread(db_session)
# processor_thread.start()

ALLOWED_NETWORKS = vision_models.__all__[-2:]

def get_allowed_layers(model_name):

    model = get_model(model_name)
    model.load_graphdef()

    # currently support only two layer types
    allowed_layers = [node.name for node in model.graph_def.node if node.op in [
        'BiasAdd', 'Conv2D']]

    return allowed_layers

# ALLOWED_LAYERS = get_allowed_layers(MODEL_NAMES)

def wrap_reply(data, success=True, data_key='data'):
    return jsonify({data_key:data, 'success':success})

@app.route('/', methods=['GET'])
def api_info():
    return jsonify({'version': api_version})


@app.route(f'/{api_version}/networks/', methods=['GET'])
def available_networks():
    '''
    Return a list of available networks
    '''
    
    reply = []
    
    for i, net in enumerate(ALLOWED_NETWORKS):
        reply.append({'id':i, 'description':NETWORK_DESCRIPTION[net], 'name':net})
    
    return wrap_reply(reply, data_key='networks')


@app.route(f'/{api_version}/networks/<network>', methods=['GET'])
def network_def(network):
    if network in ALLOWED_NETWORKS:
        return wrap_reply(get_allowed_layers(network))
    else:
        return wrap_reply(f'model {network} not found', False)

def to_url(img_name):
    im_name = img_name.split('/')[-1]
    return f'/img/{im_name}'

@app.route(f'/{api_version}/visualizations/', methods=['GET'])
def vis_all():

    vis = []
    for v in Visualization.query.all():
        d = v._asdict()

        res = []

        for r in v.results:
            dr = r._asdict()
            dr['img_url'] = to_url(dr['img_name'])
            del dr['img_name']

            res.append(dr)

        d['results'] = res

        vis.append(d)

    return wrap_reply(vis)

@app.route(f'/{api_version}/visualizations/<vis_id>', methods=['GET'])
def vis_details(vis_id):
    return jsonify({'data': [vis_id]})


def validate_params(params, required_keys=['network', 'layer']):
    for key in required_keys:
        if not key in params:
            return False

    return True

def job_to_dict(j):
    d = {
        'id': j.id,
        'status': STATUS_MAP[j.status],
        'network': j.network,
        'layer': j.layer,
        'channel': j.channel,
        'submitted': j.submitted
    }

    return d

@app.route(f'/{api_version}/jobs/', methods=['GET', 'POST'])
def jobs_all():
    if flask.request.method == 'POST':
        
        params = flask.request.get_json()

        if not validate_params(params):
            return wrap_reply('bad params', False)

        net = params['network']

        if net not in ALLOWED_NETWORKS:
            return wrap_reply(f'{net} is not allowed', False)

        layer = params['layer']

        if layer not in get_allowed_layers(net):
            return wrap_reply(f'{layer} is not allowed', False)

        if 'channel' in params:
            channel = params['channel']
        else:
            channel = ''

        j = Job(network=params['network'], layer=layer, channel=channel)
        db_session.add(j)
        db_session.commit()

        return wrap_reply('')
    else:
        jobs = []
        for j in Job.query.all():
            d = j._asdict()
            jobs.append(d)

        return wrap_reply(jobs)

@app.route('/img/<img_name>')
def get_image(img_name):
    filename = f'./imgs_generated/{img_name}'
    return send_file(filename, mimetype='image/jpg')


@app.route(f'/{api_version}/jobs/<int:job_id>', methods=['GET'])
def jobs_detail(job_id):
    job = Job.query.filter(Job.id==job_id).first()
    if not job:
        return wrap_reply(f'{job_id} not found', False)
    else:
        d = j._asdict()
        # there must be  a visualization associated object
        # if j.status == 2:
        #     d['visualization'] = j.visualization._asdict()

        return wrap_reply(d)

def run_consumer(thread):
    # db_session, Job, Visualization, VisualizationResult
    pass

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    print('running')
    app.run(debug=False, port=5001, host='0.0.0.0')  # run app in debug mode on port 5001
