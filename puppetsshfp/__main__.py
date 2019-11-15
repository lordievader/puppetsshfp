#!/usr/bin/env python3
"""Puppetdb and pdns bridge for SSHFP records
"""
import logging
from puppetsshfp import pdns
from puppetsshfp import functions


def main():
    config = functions.read_config()
    logging.basicConfig(
        level=config["loglevel"])
    logging.debug("current configuration: %s", config)

    # gather nodes from puppet db
    nodes = functions.puppet(config)
    logging.debug(nodes)

    # Init the pdns api
    powerdns = pdns.PDNS(
        config["pdns-api"],
        config["pdns-key"],
        config["pdns-zone"])

    # Check if the nodes are correct in the DNS
    dns = functions.check_nodes(nodes)

    # Add missing entries into the DNS
    if config['loglevel'] == 'DEBUG':
        import pdb
        pdb.set_trace()

    functions.add_entries(powerdns, dns)


if __name__ == '__main__':
    main()
