from api import create_app
from api.config.config import config_dict

app, socketio = create_app(config=config_dict['prod'])

if __name__ == '__main__':
    socketio.run(app)