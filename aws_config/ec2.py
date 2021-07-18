import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../additionals/'))
from access_aws_config import get_config_item

def create_security_group(ec2_client):
    """create RDS security group for public access"""

    print(f"creating RDS security group with name {get_config_item('security_group_name')}")

    return ec2_client.create_security_group(
        GroupName=get_config_item('security_group_name'),
        Description='RDS security group for public access',
        VpcId=get_config_item('security_group_vpc_id')
    )


def add_inbound_rule_to_security_group(ec2_client, security_group_id):
    """add inbound access rule to security group"""

    ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': get_config_item('inbound_access_rule_ip_protocol'),
                'FromPort': get_config_item('inbound_access_rule_from_port'),
                'ToPort': get_config_item('inbound_access_rule_to_port'),
                'IpRanges': get_config_item('inbound_access_rule_ip_ranges')
            }
        ]
    )

    print(f"added inbound access rule to security group with id: {security_group_id}")

    return None