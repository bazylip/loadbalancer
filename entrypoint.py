#!/usr/bin/python3.7

import sys
import yaml
import oyaml
from collections import OrderedDict
import nginx
import socket


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


class ConfigGenerator:
    def __init__(self, amount_of_endpoints: int, path_to_template='docker-compose-template.yml',
                 dst_port=5000, src_port=5001):
        try:
            with open(path_to_template, 'r') as file:
                self.n_endpoints = int(amount_of_endpoints)
                self.file = OrderedDict(yaml.load(file))
                self.src_port = src_port
                self.dst_port = dst_port
        except FileNotFoundError:
            print('Invalid path')
            raise SystemExit

    def generate_docker_compose(self):
        list_of_endpoints = {f'server_{str(x + 1)}': dict(self.file['services']['server_name']) for x in
                             range(self.n_endpoints)}
        for server_idx in range(self.n_endpoints):
            list_of_endpoints[f'server_{server_idx + 1}']['ports'] = [f'{self.src_port + server_idx}:{self.dst_port}']
        self.file['services']['nginx']['depends_on'] = [f'server_{str(x + 1)}' for x in range(self.n_endpoints)]
        list_of_endpoints['nginx'] = self.file['services']['nginx']
        yaml_to_save = self.file
        yaml_to_save['services'] = list_of_endpoints
        with open('docker-compose.yml', 'w') as outfile:
            oyaml.dump(yaml_to_save, outfile, default_flow_style=False)

    def generate_nginx_config(self):
        c = nginx.Conf()
        u = nginx.Upstream('loadbalancer',
                           nginx.Key('least_conn', ''))
        ip_addr = get_ip_address()
        for server_idx in range(self.n_endpoints):
            u.add(nginx.Key('server', f'{ip_addr}:{self.src_port + server_idx}'))
        s = nginx.Server(nginx.Location('/',
                                        nginx.Key('proxy_pass', 'http://loadbalancer')))
        c.add(u)
        c.add(s)
        nginx.dumpf(c, 'dockerfiles/loadbalancer/nginx.conf')


if __name__ == '__main__':
    obj = ConfigGenerator(*sys.argv[1:])
    obj.generate_docker_compose()
    obj.generate_nginx_config()
