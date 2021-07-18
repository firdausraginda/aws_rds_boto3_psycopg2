import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../additionals/'))
from access_aws_config import get_config_item
from create_boto_client import create_boto_client
from ec2 import create_security_group, add_inbound_rule_to_security_group


def create_db_subnet_group(rds_client):
    """create DB subnet group"""

    rds_client.create_db_subnet_group(
        DBSubnetGroupName=get_config_item('db_subnet_group_name'),
        DBSubnetGroupDescription='my own subnet group for RDS DB',
        SubnetIds=get_config_item('db_subnet_group_ids')
    )

    print(f"created RDS DB subnet group with name: {get_config_item('db_subnet_group_name')}")

    return None


def create_db_security_group_and_add_rules():
    """create EC2 Client, create security group, and add inbound rule to that security group"""

    # create and get ec2 client
    ec2_client = create_boto_client('ec2')

    # create security group
    security_group = create_security_group(ec2_client)

    # get id of security group
    security_group_id = security_group['GroupId']

    print(f"created RDS security group with id: {security_group_id}")

    # add public access rule to security group
    add_inbound_rule_to_security_group(ec2_client, security_group_id)

    print(f"added inbound public access rule to security group with id: {security_group_id}")

    return security_group_id


def create_postgresql_instance(rds_client):
    """create db subnet group and create db instance"""

    # retrieve security group id
    security_group_id = create_db_security_group_and_add_rules()

    # create subnet group
    create_db_subnet_group(rds_client)

    # create db instance
    rds_client.create_db_instance(
        DBName=get_config_item('db_instance_name'),
        DBInstanceIdentifier=get_config_item('db_instance_identifier'),
        DBInstanceClass=get_config_item('db_instance_class'),
        Engine=get_config_item('db_instance_engine'),
        EngineVersion=get_config_item('db_instance_engine_version'),
        Port=get_config_item('db_instance_port'),
        MasterUsername=get_config_item('db_instance_master_user_name'),
        MasterUserPassword=get_config_item('db_instance_master_user_password'),
        AllocatedStorage=get_config_item('db_instance_allocated_storage'),
        MultiAZ=get_config_item('db_instance_multi_az'),
        StorageType=get_config_item('db_instance_storage_type'),
        PubliclyAccessible=get_config_item('db_instance_publicly_accessible'),
        VpcSecurityGroupIds=[security_group_id],
        DBSubnetGroupName=get_config_item('db_instance_db_subnet_group_name')
    )

    print(f"created amazon RDS PostgreSQL DB instance with name: {get_config_item('db_instance_name')}")

    return None