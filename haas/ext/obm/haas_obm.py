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
A obm driver for using Base HaaS to execute various OBM actions on nodes 

"""

from sqlalchemy import Column, String, Integer, ForeignKey

from haas.model import Obm


class Haas_obm(Obm):
    id = Column(Integer, ForeignKey('obm.id'), primary_key=True)
    bhaas_user = Column(String, nullable=False) 
    bhaas_pass = Column(String, nullable=False)
    bhaas_proj = Column(String, nullable=False)
    
    api_name = 'http://schema.massopencloud.org/haas/v0/obm/haas_obm'
    __mapper_args__ = {
        'polymorphic_identity': api_name,
        }

