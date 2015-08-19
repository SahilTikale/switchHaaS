** Example for registering a Node which use IPMI **
Node name: dummyNoderHaaS-02
Ipmi info: hostname:- 		ipmiHost4node-02 
	   ipmi_username:-	ipmiUser4node-02
	   ipmi_password:-	ipmiPass4node-02



For nodes using IPMI use the following api call:

curl -X PUT http://127.0.0.1:5001/node/dummyNoderHaaS-02 -d '
> {"obm": { "type": "http://schema.massopencloud.org/haas/v0/obm/ipmi",
> "ipmi_host": "ipmiHost4node-02",
> "ipmi_user": "ipmiUser4node-02",
> "ipmi_password": "ipmiPass4node-02"
> }}'

