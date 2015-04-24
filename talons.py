# scraper.py - Web scraper utility
import json
import os
import time
import urllib2
import uuid

import falcon

from sqlalchemy import desc
from database import db_session, init_db
from models import *
from contextlib import closing

init_db()

api = application = falcon.API()

# _generate_id - Generates a new job ID
# @return new job ID
def _generate_id():
    return str(uuid.uuid4())

# JobManager - manages jobs for the scraper
class JobManager(object):
    # handles GET requests
    def on_get(self, req, resp, jobid):
        # check if this job ID exists
        job = db_session.query(Job).filter(Job.id == jobid).first()
        if job is not None:
            # return the results if it's done
            if job.status == 'COMPLETED':
                resp.data = json.dumps({'result':job.result})
            else:
                resp.data = json.dumps({'status':job.status})
        else:
            resp.data = json.dumps({})
            resp.status = falcon.HTTP_404

    # handle POST requests
    def on_post(self, req, resp):
        url = req.get_param('url')
        if url is not None:
            # generate a new job ID, insert it into the database, return the job ID to the client
            new_id = _generate_id()
            priority = req.get_param('priority') if req.get_param('priority') is not None else 3
            db_session.add(Job(id=new_id,status='INCOMPLETE',url=url,priority=priority,result=''))
            db_session.commit()

            # immediately tell them the job ID
            resp.data = json.dumps({'job-id':new_id})
            resp.status = falcon.HTTP_200

            # in the event that more than one requests are submitted before
            # we get to this point, this means the scraper will decide which
            # one to work with first

            # look for the most important job to do next
            next_job = db_session.query(Job).filter(Job.status == 'INCOMPLETE').order_by(desc(Job.priority),desc(Job.created)).first()
            if next_job is not None:
                # set the job as in-progress
                db_session.query(Job).filter(Job.id == next_job.id).update({"status":'IN_PROGRESS'})
                try:
                    # get the data, timeout at 30 minutes
                    response = urllib2.urlopen(next_job.url,timeout=30*60)
                    # submit the results to the database
                    db_session.query(Job).filter(Job.id == next_job.id).update({"result":response.read(),"status":'COMPLETED'})
                except urllib2.URLError, e:
                    # Python 2.6
                    if isinstance(e.reason, socket.timeout):
                        db_session.query(Job).filter(Job.id == next_job.id).update({"status":'INCOMPLETE'})
                    else:
                        # reraise the original error
                        raise
        else:
            resp.data = json.dumps({})
            resp.status = falcon.HTTP_400


job_manager = JobManager()

api.add_route('/addjob', job_manager)
api.add_route('/job/{jobid}', job_manager)
