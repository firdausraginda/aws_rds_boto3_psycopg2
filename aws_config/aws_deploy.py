from create_boto_client import create_boto_client
from rds import create_postgresql_instance

def deploy_resource():
    """create RDS client and create postgresql instance"""

    # create and get rds client
    rds_client = create_boto_client('rds')

    # create postgresql instance
    create_postgresql_instance(rds_client)

if __name__ == '__main__':
    deploy_resource()