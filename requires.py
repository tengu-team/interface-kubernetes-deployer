#!/usr/bin/env python3
# Copyright (C) 2016  Ghent University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import hashlib
from charms.reactive import when_any, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint
from charms.reactive import is_flag_set
from charmhelpers.core import unitdata


class KubernetesDeployerRequires(Endpoint):

    @when_any('endpoint.{endpoint_name}.joined')
    def deployer_joined(self):
        set_flag(self.expand_name('available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def deployer_broken(self):
        clear_flag(self.expand_name('available'))

    @when_any('endpoint.{endpoint_name}.changed.status',
              'endpoint.{endpoint_name}.changed.workers')
    def new_deployer(self):
        set_flag(self.expand_name('new-status'))
        clear_flag(self.expand_name('changed.status'))
        clear_flag(self.expand_name('changed.workers'))

    @when_any('endpoint.{endpoint_name}.departed')
    def departed(self):
        clear_flag(self.expand_name('departed'))

    def get_status(self):
        status = {}
        for relation in self.relations:
            for unit in relation.units:
                if not unit.received['status']:
                    continue
                status ={
                    'status': unit.received['status'],
                    'remote_unit_name': unit.unit_name,
                }
        return status

    def get_worker_ips(self):
        ips = []
        for relation in self.relations:
            for unit in relation.units:
                ips = unit.received['workers']
        return ips

    def send_create_request(self, resource):
        # Resource should be a list with dicts, one per resource
        for relation in self.relations:
            relation.to_publish['resource'] = resource
            relation.to_publish['uuid'] = self.get_uuid()
            relation.to_publish['model_uuid'] = os.environ['JUJU_MODEL_UUID']
            relation.to_publish['juju_unit'] = os.environ['JUJU_UNIT_NAME'].split('/')[0]

    def get_uuid(self):
        """
        Returns a UUID for this juju application by 
        taking the MD5 hash of the juju application name.

        The juju model uuid + juju application name is used 
        to prevent cross model collisions.
        """
        k8s_uuid = unitdata.kv().get('k8s_uuid', None)
        if not k8s_uuid:
            juju_model = os.environ['JUJU_MODEL_UUID']
            juju_app_name = os.environ['JUJU_UNIT_NAME'].split('/')[0]
            unique_name = juju_model + juju_app_name
            k8s_uuid = hashlib.md5(unique_name.encode('utf-8')).hexdigest()
            unitdata.kv().set('k8s_uuid', k8s_uuid)
        return k8s_uuid
