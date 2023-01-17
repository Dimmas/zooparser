#!/usr/bin/env python
#coding: utf-8

from helpers import get_logger, Vscale_Helper
from settings import config
import time
import yaml
from ansible_runner import Runner, RunnerConfig

main_logger = get_logger(__name__)


if __name__ == '__main__':
    # Create nodes into vscale-provider
    """vs = Vscale_Helper(client_id=config.VSCALE_CID, api_key=config.VSCALE_API_KEY)
    target_image = [image for image in vs.images_list() if 'docker' in image['id']][0]
    for i in range(config.PROXIES_COUNT):
        vs.scalet_create(
            name=f'node_{i}',
            plan=target_image['rplans'][2] if i == 0 else target_image['rplans'][0],
            image=target_image['id'],
            location=target_image['locations'][0],
            keys=[key['id'] for key in vs.sshkey_list()],
            autostart=True
        )

    time.sleep(30)
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
        gv.truncate()

    time.sleep(60)"""

    # Using tag using RunnerConfig
    rc = RunnerConfig(
        private_data_dir="ansible",
        playbook="kuber_playbook.yml"
    )
    rc.prepare()
    r = Runner(config=rc)
    r.run()
