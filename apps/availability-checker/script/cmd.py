#!/usr/bin/env python3

import argparse
import zmq
import requests
import os
import logging
import sys
import time

from kubernetes import client, config
from kubernetes.client.rest import ApiException

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

class KubernetesClient():

    def _load_k8s_config(self):
        try:
            config.load_incluster_config()
            logging.info('Loaded in-cluster kubernetes config')
        except config.ConfigException:
            config.load_kube_config()
            logging.info('Loaded local kubernetes config')

    def start(self):
        pass

    def stop(self):
        pass

class Server(KubernetesClient):

    VALID_HTTP_CODES = [200]

    def __init__(self, port:int = 5556, topic_id:int = 1, sleep_time_s:int = 60):
        self.__port = port
        self.__topic_id = topic_id
        self.__enabled = False
        self.__sleep_time_s = sleep_time_s

    def _get_ingresses_hosts(self):
        api_client = client.NetworkingV1Api()
        try:
            ingress_list = api_client.list_ingress_for_all_namespaces(allow_watch_bookmarks=True)
            logging.info('Loaded list of ingresses')
        except ApiException as e:
            logging.info(f"Couldn't load list of ingresses, see errror below:\n{str(e)}")
            return
            yield
        for ingress in ingress_list.items:
            for rule in ingress.spec.rules:
                if rule.host:
                    yield rule.host

    def start(self):
        self._load_k8s_config()
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(f'tcp://*:{self.__port}')
        logging.info(f"Binded to 'tcp://*:{self.__port}'")
        self.__enabled = True
        while self.__enabled:
            status_codes = {}
            for host in self._get_ingresses_hosts():
                url = f'https://{host}'
                try:
                    r = requests.get(url)
                    logging.info(f"Request to url:'{url}' finished with '{r.status_code}' status code")
                    status_codes[host] = r.status_code in Server.VALID_HTTP_CODES
                except requests.exceptions.ConnectionError as e:
                    logging.warning(f"Problem calling url:'{url}', see error below:\n{str(e)}")
            if status_codes and not any(status_codes.values()):
                logging.info('All hosts unavailable, sending reboot request!')
                socket.send_string(f'{self.__topic_id} reboot')
            logging.info(f'Sleeping for {self.__sleep_time_s}s')
            time.sleep(self.__sleep_time_s)

    def stop(self):
        self.__enabled = False

class Client(KubernetesClient):

    def __init__(self, host='localhost', port=5556, topic_id=1):
        self.__host = host
        self.__port = port
        self.__topic_id = topic_id
        self.__enabled = False

    def start(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(f'tcp://{self.__host}:{self.__port}')
        socket.setsockopt(zmq.SUBSCRIBE, f'{self.__topic_id}'.encode('utf8'))
        logging.info(f"Connected to 'tcp://{self.__host}:{self.__port}'")
        self.__enabled = True
        while self.__enabled:
            topic, message = socket.recv().decode('ASCII').split()
            if message == 'reboot':
                logging.info('Received reboot request!')
                os.popen('/bin/systemctl reboot')


    def stop(self):
        self.__enabled = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5556, required=False, help='Port for ZMQ sub/pub')
    parser.add_argument('-t', '--topic', type=int, default=1, required=False, help='Topic for ZMQ sub/pub')
    subparsers = parser.add_subparsers(dest="subparser")
    client_parser = subparsers.add_parser("client")
    client_parser.add_argument('-u', '--host', type=str, default='localhost', required=False, help='Host for ZMQ sub')
    server_parser = subparsers.add_parser("server")
    server_parser.add_argument('-s', '--sleep-time', type=int, default=10, required=False, help='Host for ZMQ sub')

    args = parser.parse_args(sys.argv[1:])

    if args.subparser == 'client':
        cmd = Client(args.host, args.port, args.topic)
        cmd.start()
    elif args.subparser == 'server':
        cmd = Server(args.port, args.topic, args.sleep_time)
        cmd.start()
    else:
        parser.print_help()
        exit()
    
    cmd.stop()
