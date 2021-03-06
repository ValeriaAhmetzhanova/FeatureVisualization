# import threading
import time

from models import Job, Visualization, VisualizationResult
from database import db_session

from lucid.modelzoo.nets_factory import get_model
import lucid.optvis.render as render
import lucid.optvis.transform as transform
import lucid.optvis.param as param

import tensorflow as tf

import scipy.misc


def _grab_job():
    return Job.query.filter(Job.status == 0).first()


def _process_job(job):
    network = job.network
    layer = job.layer
    channel = job.channel

    if not len(channel):
        channel = '0'

    target = f'{layer}:{channel}'

    print(f'running a job with {network}, {target}')

    # `fft` parameter controls spatial decorrelation
    # `decorrelate` parameter controls channel decorrelation
    param_f = lambda: param.image(256, fft=True, decorrelate=True)
    transforms = transform.standard_transforms

    optimizer = tf.train.AdamOptimizer(0.05)
    
    model = get_model(network)
    model.load_graphdef()

    results = render.render_vis(model, target,
                             optimizer=optimizer,
                             transforms=transforms,
                             param_f=param_f, verbose=True,
                             thresholds=(2048,))

    vis = Visualization(job)
    
    db_session.add(vis)

    for i, img in enumerate(results):
        print(img.shape)
        name = f'./imgs_generated/{job.submitted}-{i}.jpg'
        scipy.misc.imsave(name, img.squeeze())

        vis_r = VisualizationResult(name, vis)

        db_session.add(vis_r)

    job.status = 2
    db_session.add(job)

    db_session.commit()


    del model
    del results


if __name__ == "__main__":

    while True:
        job = _grab_job()

        if job:
            _process_job(job)

        time.sleep(1.0)