from flask import Flask
from celery import Celery

CELERY_TASK_LIST = [
    'proj.app.tasks',
]

def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('proj.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    extensions(app)

    return app


@celery.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# Routes

@app.route('/text', methods=['GET'])
def text():

	num_workers = 5

	data_paths = ["/home/ubuntu/data/05cb5036-2170-401b-947d-68f9191b21c6",
				  "/home/ubuntu/data/094b1612-1832-429e-98c1-ae06e56d88d6", 
				  "/home/ubuntu/data/0c7526e6-ce8c-4e59-884c-5a15bbca5eb3",
				  "/home/ubuntu/data/0d7c752e-d2a6-474b-aef4-afe5dc506e33",
				  "/home/ubuntu/data/0ecdf8e0-bc1a-4fb3-a015-9b8dc563a92f"]

	result = return_text.delay(data_paths[0])

	print "Task finished? ", str(result.ready())
	print "Task result ", result.result

	time.sleep(10)

	print "Task finished? " + str(result.ready())
	print "Task result ", result.result


	return result.result

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5000)