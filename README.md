# aws_rds_boto3_psycopg2

# Create Credential Files

### aws_config.json

Need to create `aws_config.json` file, contains AWS configuration:

```
{
    "region_name": "<region_name>",
    "aws_access_key_id": "<aws_access_key_id>",
    "aws_secret_access_key": "<aws_secret_access_key>",

    "security_group_name": "<security_group_name>",
    "security_group_vpc_id": "<security_group_vpc_id>",

    "inbound_access_rule_ip_protocol": "<inbound_access_rule_ip_protocol>",
    "inbound_access_rule_from_port": "<inbound_access_rule_from_port>",
    "inbound_access_rule_to_port": "<inbound_access_rule_to_port>",
    "inbound_access_rule_ip_ranges": "<inbound_access_rule_ip_ranges>",

    "db_subnet_group_name": "<db_subnet_group_name>",
    "db_subnet_group_ids": "<db_subnet_group_ids>",

    "db_instance_name": "<db_instance_name>",
    "db_instance_identifier": "<db_instance_identifier>",
    "db_instance_class": "<db_instance_class>",
    "db_instance_engine": "<db_instance_engine>",
    "db_instance_engine_version": "<db_instance_engine_version>",
    "db_instance_port": "<db_instance_port>",
    "db_instance_master_user_name": "<db_instance_master_user_name>",
    "db_instance_master_user_password": "<db_instance_master_user_password>",
    "db_instance_allocated_storage": "<db_instance_allocated_storage>",
    "db_instance_multi_az": "<db_instance_multi_az>",
    "db_instance_storage_type": "<db_instance_storage_type>",
    "db_instance_publicly_accessible": "<db_instance_publicly_accessible>",
    "db_instance_db_subnet_group_name": "<db_instance_db_subnet_group_name>"
}
```

### database.ini

Need to create `database.ini` file, contains database configuration:

```
[postgresql]
database=<database_name>
host=<host>
port=<port>
user=<master_user_name>
password=<master_user_password>
```

# Usage

To run script that set AWS config:

```
pipenv run python aws_config/main.py -c aws_config.json
```