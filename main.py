#!/usr/bin/env python
#coding: utf-8

from parsers import CatalogParser, CategoryParser
from helpers import get_logger, Vscale_Helper
from settings import config
import time
from ansible_runner import Runner, RunnerConfig
import yaml

main_logger = get_logger(__name__)


def restarter(fn):
    def wrapper(*args, **kwargs):
        for _ in range(config.RESTART_COUNT):
            try:
                return fn(*args, **kwargs)
            except:
                print('Critical error. Parser would be restarted.')
                main_logger.exception('exception')
                time.sleep(config.RESTART_INTERVAL*60)
    return wrapper


@restarter
def parse_catalog():
    with CatalogParser(source) as cat_parser:
        return cat_parser.parse_catalog(subcatalog=config.CATEGORIES)


@restarter
def parse_categories(ctlg_href_set: set):
    with CategoryParser(source) as cat_parser:
        return cat_parser.parse_categories(ctlg_href_set)


if __name__ == '__main__':
    source = 'https://zootovary.ru/'

# Create nodes into vscale-provider
    vs = Vscale_Helper(client_id=config.VSCALE_CID, api_key=config.VSCALE_API_KEY)
    target_image = [image for image in vs.images_list() if 'docker' in image['id']][0]

    """for i in range(config.PROXIES_COUNT):
        vs.scalet_create(
            name=f'node_{i}',
            plan=target_image['rplans'][0],
            image=target_image['id'],
            location=target_image['locations'][0],
            keys=[key['id'] for key in vs.sshkey_list()],
            autostart=True
        )

    time.sleep(60)
    scalets_list = vs.scalets_list()
    scalets_ip_list = [scalet['public_address']['address'] for scalet in scalets_list]
    master_node = scalets_ip_list[0]

    with open('ansible/hosts.txt', 'w') as f:
        f.write('[masters]\n')
        f.write(master_node)
        f.write('\n[workers]\n')
        f.writelines(scalets_ip_list[1:])

    with open('ansible/group_vars/all', 'r+') as gv:
        group_all_vars = yaml.load(gv, Loader=yaml.FullLoader)
        group_all_vars['k8s_master_ip'] = master_node
        gv.seek(0)
        yaml.dump(group_all_vars, gv, default_flow_style=False)
        gv.truncate()"""

    # Using tag using RunnerConfig
    rc = RunnerConfig(
        private_data_dir="ansible",
        playbook="kuber_playbook.yml"
    )

    rc.prepare()
    r = Runner(config=rc)
    r.run()

# deploy my containers

#Start parse site
    """ctlg_href_set = parse_catalog()

    if ctlg_href_set:
        parse_categories(ctlg_href_set)
"""