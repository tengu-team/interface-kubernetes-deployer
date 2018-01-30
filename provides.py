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


class KubernetesDeployerProvides(Endpoint):

    @when_any('endpoint.{endpoint_name}.joined')
    def request_joined(self):
        set_flag(self.expand_name('available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def no_request_joined(self):
        clear_flag(self.expand_name('available'))
        clear_flag(self.expand_name('departed'))

    @when_any('endpoint.{endpoint_name}.changed.resource')
    def new_resource_request(self):
        set_flag(self.expand_name('new-resource'))
        clear_flag(self.expand_name('changed.resource'))

    def get_resource_requests(self):
        # Returns resource requests of ALL connected k8s charms
        resource_requests = []
        for relation in self.relations:
            for unit in relation.units:
                resource_requests.append({
                    'resource': unit.received['resource'],
                    'remote_unit_name': unit.unit_name
                })
        return resource_requests

    def send_status(self, status):
        # Send status of the resources
        for relation in self.relations:
            relation.to_publish['status'] = status

    def send_worker_ips(self, workers):
        # Send Ips of k8s workers
        for relation in self.relations:
            relation.to_publish['workers'] = workers
