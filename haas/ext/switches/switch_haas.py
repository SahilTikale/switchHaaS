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

"""A switch driver for recursive HaaS
It will run the necessary commands on the bHaaS to provide the switch 
related configuration activities. 

"""
from sqlalchemy import Column, String, Integer, ForeignKey
from haas.model import Switch


class Switch_haas(Switch):
    api_name = 'http://schema.massopencloud.org/haas/v0/switches/switch_haas'

    __mapper_args__ = {
            'polymorphic_identity': api_name,
            }
    id = Column(Integer, ForeignKey('switch.id'), primary_key=True)



