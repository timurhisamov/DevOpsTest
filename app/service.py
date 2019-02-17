from flask import Flask, request, json
from apscheduler.schedulers import background
import atexit, yaml
import requests

class Config:
    def __init__(self, jenkins_url, jenkins_user, jenkins_pass, jobs):
        self.jenkins_url = jenkins_url
        self.jenkins_user = jenkins_user
        self.jenkins_pass = jenkins_pass
        self.jobs = jobs

    def __repr__(self):
        return "%s(jenkins_url=%r, jenkins_user=%r, jenkins_pass=%r, jobs=%r)" % \
               (self.__class__.__name__, self.jenkins_url, self.jenkins_user, self.jenkins_pass, self.jobs)

def create_app():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-conf')
    args = parser.parse_args()
    app = Flask(__name__)
    app.config['config_file_uri'] = args.conf
    return app


def read_config():
    print("Reading config...")
    with open(app.config['config_file_uri'], 'r') as stream:
        try:
            app.config['config'] = yaml.load(f"!!python/object:__main__.Config\n{stream.read()}")
            print(app.config['config'].__repr__())
        except yaml.YAMLError as exc:
            print(exc)


def send_post(jobs, params):
    parameters = {'parameter': []}
    for param_key in params.keys():
        parameters.get('parameter').append({'name': param_key, 'value': params.get(param_key)})

    has_error = False
    for job in jobs:
        jenkins_build_url = "%s/job/%s/build" % (app.config['config'].jenkins_url, job.get('job_name'))
        print("Sending post request to URL: " + jenkins_build_url)
        print("With parameters: " + str(parameters))
        r = requests.post(jenkins_build_url,
                          data=parameters,
                          auth=(app.config['config'].jenkins_user, app.config['config'].jenkins_pass))
        print(r.status_code, r.reason)
        if r.status_code >= 200 & r.status_code < 300:
            has_error = True
    return has_error


app = create_app()

scheduler = background.BackgroundScheduler()
scheduler.add_job(func=read_config, trigger="interval", seconds=60)
scheduler.start()


@app.route('/')
def home_page():
    return 'DevOpsTest Task is working!'


@app.route('/post', methods=['POST'])
def post():
    data = json.loads(request.data)
    print(data)
    project = data.get('project')
    jobs_to_do = []
    for job in app.config['config'].jobs:
        for proj in job.get('projects'):
            if proj == project:
                jobs_to_do.append(job)
    print("Jobs to send: " + str(jobs_to_do))
    send_post(jobs_to_do, data.get('params'))
    return "OK" #TODO Return normal response


atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    read_config()
    app.run(host='0.0.0.0')