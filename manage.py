from flask_script import Manager

from app import create_app

application = None

if __name__ == '__main__':
    application = create_app()
    manager = Manager(application)
else:
    manager = Manager()


@manager.command
def start():
    application.debug = True
    application.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    manager.run()
