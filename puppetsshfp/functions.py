"""Puppetdb and pdns bridge for SSHFP records
"""
import os
import logging
import pdb
import pypuppetdb
import yaml


def puppet(config):
    """Query puppetdb for details about hosts.

    :param config: configuration dictionary
    :type config: dictionary
    """
    puppetdb_config = {}
    for key, value in config.items():
        if key.startswith("puppetdb"):
            puppetdb_config[key.replace("puppetdb-", "")] = value

    logging.debug("PuppetDB configuration: %s", puppetdb_config)
    puppetdb = pypuppetdb.connect(**puppetdb_config)
    nodes = {}
    keywords = {
        'sshfp_rsa': 'sshfp_rsa',
        'sshfp_dsa': 'sshfp_dsa',
        'sshfp_ecdsa': 'sshfp_ecdsa',
        'sshfp_ed25519': 'sshfp_ed25519',
    }
    for key, value in keywords.items():
        facts = puppetdb.facts(key)
        for fact in facts:
            node_name = fact.node
            ip_address = fact.value
            if node_name in nodes:
                nodes[node_name][value] = ip_address

            else:
                nodes[node_name] = {value: ip_address}

    return nodes


def check_nodes(nodes):
    """This function checks if the DNS records match with what is in Puppet.
    """
    keywords = {
        'sshfp_rsa': 'SSHFP',
        'sshfp_dsa': 'SSHFP',
        'sshfp_ecdsa': 'SSHFP',
        'sshfp_ed25519': 'SSHFP',
    }
    dns = {}
    for node, addresses in nodes.items():
        if node not in dns:
            dns[node] = {}

        for key, value in keywords.items():
            if key not in addresses:
                continue

            dns_value = addresses[key]
            if key.startswith('sshfp'):
                dns_value = [item.replace('SSHFP ', '')
                             for item in dns_value.split('\n')]

            else:
                dns_value = [dns_value]

            if value in dns[node]:
                dns[node][value].extend(dns_value)

            else:
                dns[node][value] = dns_value

            logging.info('%s: %s -> %s', key, value, dns_value)

    logging.info(dns)
    return dns


def add_entries(pdns, dns):
    """Function for adding DNS records to PowerDNS.
    """
    for label, records in dns.items():
        for record_type, values in records.items():
            logging.info("%s %s %s", label, record_type, values)
            pdns.add(label, record_type, values)


def read_config():
    """Reads a config.yml from the root directory.
    """
    path = os.path.join(
        os.path.curdir,
        "config.yml")
    with open(path, "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.Loader)

    return config
