#!/usr/bin/env python
"""
Asterisk Fabfile
================
"""
import fabric.api as fapi
from fabric.context_managers import env, cd, settings
from fabric.decorators import hosts

def _load_hosts():
    with open('../inventory/hosts') as fd:
        lines = [line.strip() for line in fd.readlines() if 'utqansible' in line]
    hosts = []
    passwords = {}
    for line in lines:
        if 'surveysampling.com' in line:
            host = "root@{}:22".format(line)
            name = host.split('@')[1].split('.')[0]
            password = "G04{}!".format(name)
            hosts.append(host)
            passwords[host] = password
    return hosts, passwords

env.hosts, env.passwords = _load_hosts()


def install_ansible():
    """
    Each server should have:

    """
    with settings(warn_only=True):
        # Create the 'git' user if it doesn't exist
        fapi.run("adduser -s /bin/bash -m git")
        fapi.run("mkdir -p /home/git/.ssh")
        fapi.put("setup/sudoers.d_cati", "/etc/sudoers.d/cati_deploy")
        with cd("/home/git/.ssh"):
            fapi.put("setup/ssh_config", "config")
            fapi.put("setup/authorized_keys", "authorized_keys")
            fapi.put("setup/ssh_id_rsa", "github_id_rsa")

        fapi.run("chown -R git:git /home/git")
        fapi.run("chmod -R 0644 /home/git/.ssh/*")
        fapi.run("chmod -R 0600 /home/git/.ssh/github_id_rsa")

    # Install ansible
    fapi.run("yum install -y ansible")
