# coding=utf-8
from argparse import ArgumentParser

import server


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', default='config', type=str,
                        help='config file name')
    args = parser.parse_args()
    config_filename = args.config

    app = server.app
    app.config.from_object(config_filename)
    app.config['CONFIG_FILENAME'] = config_filename
    server.init()

    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        use_reloader=app.config['USE_RELOADER']
    )
