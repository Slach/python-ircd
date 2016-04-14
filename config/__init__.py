import os
from six.moves.configparser import SafeConfigParser
from datetime import datetime
from pydispatch import dispatcher
import logging.config
import argparse

__all__ = ['config']

class SignalingSafeConfigParser(SafeConfigParser):
    def set(self, section, option, value=None):
        SafeConfigParser.set(self, section, option, value)
        dispatcher.send('%s.%s' % (section, option), 'config')


parser = argparse.ArgumentParser(description='python-ircd running script')
parser.add_argument('--config-path',
                    type=str,
                    required=False,
                    help='path to the server.ini and logging.ini')
args = parser.parse_args()

config_path = args.config_path if args.config_path else os.path.dirname(__file__)
config = SignalingSafeConfigParser({
    'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
})
config.read(os.path.join(config_path, 'server.ini'))


logging.config.fileConfig(os.path.join(
    config_path, 'logging.ini'
))
