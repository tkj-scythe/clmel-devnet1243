
import sys
import logging
from ncclient import manager



UPDATE_RBACL = """
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <cts>
            <role-based xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-cts">
                <permissions>
                    <from>
                        <range>
                            <range>{src_sgt}</range>
                            <to>
                                <range>
                                    <range>{dst_sgt}</range>
                                    <ACL-name-new>{acl_name}</ACL-name-new>
                                    <ACL-name>{acl_name}</ACL-name>
                                    <name>{acl_name}</name>
                                </range>
                            </to>
                        </range>
                    </from>
                </permissions>
            </role-based>
        </cts>
    </native>
</config>
"""

def iosxe_connect(host, port, user, password):
    return manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           device_params={'name': "iosxe"},
                           timeout=30,
                           hostkey_verify=False
            )

def export_config(host, user, password):
    with iosxe_connect(host, port=830, user=user, password=password) as m:
        config = m.get_config(source='running')
        with open("output.xml", "w") as f:
            f.write(config.xml)


def update_rbacl(host, user, password, acl_name, src_sgt, dst_sgt):
    confstr = UPDATE_RBACL.format(acl_name = acl_name, src_sgt = src_sgt, dst_sgt = dst_sgt)
    with iosxe_connect(host, port=830, user=user, password=password) as m:
        m.edit_config(target='running', config=confstr)

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    #ARG are: host username password function_name [function dependant]
    if (sys.argv[4] == "update_rbacl"):
        update_rbacl(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[5], sys.argv[6], sys.argv[7])
    elif (sys.argv[4] == "export_config"):
        export_config(sys.argv[1], sys.argv[2], sys.argv[3])
