#!/usr/bin/env python3
"""Provides a wrapper for talking to the powerdns api.
"""
import logging
import powerdns


class PDNS():
    """Wrapper to talk to the PDNS api.
    """
    def __init__(self, api, key, zone):
        self.api_client = powerdns.PDNSApiClient(api_endpoint=api, api_key=key)
        self.api = powerdns.PDNSEndpoint(self.api_client)
        self.zone_name = zone
        self.zone = self.api.servers[0].get_zone(zone)

    def search(self, name, rtype='SSHFP'):
        """Search the zone for a specified record.
        """
        extended_name = '.'.join([name, self.zone_name])
        records = []
        for record in self.zone.details['rrsets']:
            if ((name == record['name'] or extended_name == record['name'])
                    and rtype == record['type']):
                records.append(record)

        return records

    def add(self, name, rtype, values, ttl=3600):
        """Add a new record to the zone.

        :param name: label name
        :type name: str
        :param rtype: type of record
        :type rtype: str
        :param values: values of label
        :type values: list
        :param ttl: time to live
        :type ttl: int
        """
        if name.endswith('.'):
            extended_name = name

        else:
            extended_name = '{name}.'.format(name=name)

        logging.info(
            'Adding record: %-30s %3s %20s %4d',
            extended_name, rtype, values, ttl)
        items = [(item, False) for item in values]
        rrset = powerdns.RRSet(extended_name, rtype, items, ttl=ttl)
        self.zone.create_records([rrset])
