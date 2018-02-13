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

from charms.reactive import when_any, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint
from charms.reactive import is_flag_set


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
        status = []
        for relation in self.relations:
            for unit in relation.units:
                status.append({
                    'status': unit.received['status'],
                    'remote_unit_name': unit.unit_name,
                })
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
