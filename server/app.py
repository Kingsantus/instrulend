from api import create_app, socketio
from api.config.config import config_dict

app = create_app(config=config_dict['prod'])

if __name__ == '__main__':
    socketio.run(app)