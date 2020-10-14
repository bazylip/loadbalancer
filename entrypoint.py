#!/usr/bin/python3.7

import sys
import yaml
from collections import OrderedDict


class DockerCompose:
    def __init__(self, amount_of_endpoints: int, path_to_template='docker-compose-template.yml',
                 dst_port=5000, src_port=5001):
        try:
            with open(path_to_template, 'r') as file:
                self.n_endpoints = int(amount_of_endpoints)
                self.file = OrderedDict(yaml.load(file))
                self.src_port = src_port
                self.dst_port = dst_port
                print(self.file)
        except FileNotFoundError as e:
            print('Invalid path')

    def generate_docker_compose(self):
        list_of_endpoints = {f'server_{str(x+1)}': dict(self.file['services']['server_name']) for x in range(self.n_endpoints)}
        for server_idx in range(self.n_endpoints):
            list_of_endpoints[f'server_{server_idx+1}']['ports'] = [f'{self.src_port+server_idx}:{self.dst_port}']
        self.file['services']['nginx']['depends_on'] = [f'server_{str(x+1)}' for x in range(self.n_endpoints)]
        list_of_endpoints['nginx'] = self.file['services']['nginx']
        yaml_to_save = self.file
        yaml_to_save['services'] = list_of_endpoints
        with open('docker-compose-test.yml', 'w') as outfile:
            yaml.dump(dict(yaml_to_save), outfile, default_flow_style=False)

if __name__ == '__main__':
    obj = DockerCompose(*sys.argv[1:])
    obj.generate_docker_compose()