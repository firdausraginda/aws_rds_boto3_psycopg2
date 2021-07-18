import boto3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../additionals/'))
from access_aws_config import get_config_item

def create_boto_client(aws_service):
    """create EC2/RDS client"""

    client = boto3.client(
        aws_service,
        region_name=get_config_item('region_name'),
        aws_access_key_id=get_config_item('aws_access_key_id'),
        aws_secret_access_key=get_config_item('aws_secret_access_key')
    )

    return client