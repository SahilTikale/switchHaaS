# Copyright 2013-2014 Massachusetts Open Cloud Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language
# governing permissions and limitations under the License.

"""
A obm driver for implementing lego robot based controls for 
arm based servers on in a DC at North Pole :-)

"""

from sqlalchemy import Column, String, Integer, ForeignKey
import schema


from haas.model import Obm
from haas.errors import OBMError
from haas.dev_support import no_dry_run

class Ipmi(Obm):
    id = Column(Integer, ForeignKey('obm.id'), primary_key=True)
    ipmi_host = Column(String, nullable=False) 
    ipmi_user = Column(String, nullable=False)
    ipmi_password = Column(String, nullable=False)

    api_name = 'http://schema.massopencloud.org/haas/v0/obm/ipmi'
    __mapper_args__ = {
        'polymorphic_identity': api_name,
        }
    @staticmethod
    def validate(kwargs):
        schema.Schema({
            'type': Ipmi.api_name,
            'ipmi_host': basestring,
            'ipmi_user': basestring,
            'ipmi_password': basestring,
            }).validate(kwargs)

    def _ipmitool(self, args):
        """ Invoke ipmitool with the right host/pass etc. for this code.
        `args`- A list of any additional arguments to pass the ipmitool. 
        Returns the exit status of ipmitool.
        """
        status = call(['ipmitool',
        '-U', self.ipmi_user,
        '-P', self.ipmi_pass,
        '-H', self.ipmi_host]  + args)
        
        if status != 0:
            logger = logging.getLogger(__name__)
            logger.info('Nonzero exit status form ipmitool, args = %r', args)
        return status

    @no_dry_run
    def power_cycle(self):
        """
        Reboot the node via ipmi. 
        Returns True if successful, False othewise.
        """
        self._ipmitool(['chassis', 'bootdev', 'pxe'])
        if self._ipmitool(['chassis', 'power', 'cycle']) == 0:
            return
        if self._ipmitool(['chassis', 'power', 'on']) == 0:
            # power cycle will fail if the machine is not running.
            # It is a good idea to turn it on, that way we can save
            # save power by turning things off without breaking the HaaS
            return
        #If this fails then it is a real problem
        raise OBMError('Could not power cycle node %s' % self.node.label)
