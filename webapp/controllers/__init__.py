from .mainController import *
from .workerListController import *
from .workerManagementController import *


def init_app(app):
    app.register_blueprint(main)
    app.register_blueprint(workerList)
    app.register_blueprint(workerManagement)
    return app
