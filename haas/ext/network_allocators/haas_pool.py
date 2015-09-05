# Copyright 2013-2014 Massachusetts Open Cloud Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.
"""A network allocator for recursive HaaS

Network IDs are generated at random and serve as network names
for base HaaS
"""
import logging
import uuid

from sqlalchemy import Column, String, Integer, Boolean

from haas.config import cfg
from haas import model
from haas.model import AnonModel
from haas.network_allocator import NetworkAllocator, set_network_allocator


db = model.Session()


class HaasVlanAllocator(NetworkAllocator):
    """An allocator of vlans to recursive HaaS.

    The interface is as specified in ``NetworkAllocator``.
    """

    def get_new_network_id(self, db):
        """Creates a UUID for a new vlan and

        1.) populate the haas_netid table in the database.
        This string will be used as label to the base HaaS.
        """
        newNetid = "rhaas-"+str(uuid.uuid4())
        add_netid = HaaS_Netid(net_id=newNetid)
        db.add(add_netid)
        db.commit()
        return newNetid

    def free_network_id(self, db, bhaas_netname):
        bhaas_netName = db.query(HaaS_Netid).filter(HaaS_Netid.net_id==bhaas_netname).first()
        if not bhaas_netName:
            logger = logging.getLogger(__name__)
            logger.error('vlan %s does not exist in database' % net_id)
            return
        db.delete(bhaas_netName)
        db.commit()

    def populate(self, db):
        """Recursive HaaS does not require this function.

        Keeping it for compliance as a subclass.
        """
        pass

    def legal_channels_for(self, db, net_id):
        """Recursive Haas depends on Base HaaS for its values.

        So it would be null in this case.
        """
        return ["null"]

    def is_legal_channel_for(self, db, channel_id, net_id):
        return channel_id == "null"

    def get_default_channel(self, db):
        return "null"


class HaaS_Netid(AnonModel):
    """This table will contain names of network in base HaaS

    For every network created under recursive HaaS, it will generate
    new network id in the form of a random string appended to "rhaas"
    and store this string in this table
    """

    net_id = Column(String, nullable=False, unique=True)


def setup(*args, **kwargs):
    set_network_allocator(HaasVlanAllocator())
