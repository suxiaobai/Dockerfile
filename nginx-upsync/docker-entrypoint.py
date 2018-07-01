#!/usr/bin/env python
# o_o coding: utf-8 o_o
# auth xiaobai
#
###############################################

import os
import logging
import json
from string   import Template
from optparse import OptionParser
import argparse

logging.basicConfig(format='[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]', datefmt='%Y/%m/%d %I:%M:%S')

def file_slave(path,data):
    try:
        with open(path, 'w') as F:
            F.write(data)
    except Exception as identifier:
        logging.error('File Write Error: %s' % identifier)


def get_services(consul_host, consul_port, upstream_path):
    upstream_config = '''
    upstream $service {
        server 127.0.0.1:18882;
        upsync $consul_host:$consul_port/v1/health/service/$service upsync_timeout=6m upsync_interval=500ms upsync_type=consul_health strong_dependency=off;
        upsync_dump_path /data/apps/config/nginx/conf.d/upstreams/$service.conf;
    }

    '''
    ups = '''# upsync upstream config \n'''
    url = 'http://%s:%s/v1/catalog/services' % (consul_host, consul_port)
    try:
        services = json.loads(os.popen('curl %s' % url).read())
        for i in services:
            d = dict(service=i, consul_host=consul_host, consul_port=consul_port)
            ups = ups + Template(upstream_config).safe_substitute(d)
        file_slave(upstream_path, ups)
    except Exception as identifier:
        logging.error(
            'Consul address invalid or service is null in consul: %s' % identifier)

def nginx_start():
    try:
        os.system("/data/apps/opt/nginx/sbin/nginx -g daemon off;")
    except Exception as identifier:
        logging.error('Start nginx Error: %s' % identifier)

def read_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-O', dest='option')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    consul_host = os.environ.get('host') or '127.0.0.1'
    consul_port = os.environ.get('port') or '8500'
    upstream_path = os.environ.get(
        'upsfile') or '/data/apps/config/nginx/conf.d/dyups.upstream.kefu.eaemob.com.conf'
    services = os.environ.get('services')
    args = read_cli_args()
    if args.option == 'start':
        get_services(consul_host, consul_port, upstream_path)
        os.system('/data/apps/opt/nginx/sbin/nginx -g "daemon off;"')

    if args.option == 'reload':
        get_services(consul_host, consul_port, upstream_path)
        os.system("/data/apps/opt/nginx/sbin/nginx -s reload")
