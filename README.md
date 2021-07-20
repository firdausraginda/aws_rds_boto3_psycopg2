# aws_rds_boto3_psycopg2

# Create Credential Files

If you are **familiar** with AWS RDS & PostgreSQL DB, I've compiled the configuration in 2 files for central setup: `aws_config.json` & `database.ini`. Can just create those 2 files in the root directory before run the program.
If this is your **first time** using AWS RDS, kindly jump to the **AWS Depedencies** section below and follow the steps there.

**1. aws_config.json**
In `aws_config.json` file, kindly fill the AWS configurations:

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

**2. database.ini**
In `database.ini` file, kindly fill the PostgreSQL database configurations:

```
[postgresql]
database=<database_name>
host=<host>
port=<port>
user=<master_user_name>
password=<master_user_password>
```

# Python Depedencies

Install depedencies using **[pipenv](https://pipenv.pypa.io/en/latest/install/)** as depedency manager.

For automatic dependency installation, can just run:
`> pipenv sync`

If still encounter **ModuleNotFoundError** later on, can do it manually instead:

1. Install [Boto3](https://pypi.org/project/boto3/)
`> pipenv install boto3`

2. Install [Psycopg2](https://pypi.org/project/psycopg2/)
`> pipenv install psycopg2`

# Usage

Command to deploy AWS config already compiled in `aws_config/aws_deploy.py`, to run that file can simply type :

```
pipenv run python aws_config/aws_deploy.py -c aws_config.json
```

Command to access the PostgreSQL DB compiled in `db_config/db_access.py`, to run that file:
```
pipenv run python db_config/db_access.py
```

# AWS Depedencies

These are steps to set configuration on AWS platform:

**1. Create AWS Account**

For personal project purpose, can just create free AWS account [here](https://portal.aws.amazon.com/billing/signup?refid=em_127222&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start).

**2. Create New User**

After create AWS account, login to [AWS Management Console](https://aws.amazon.com/id/console/) using that account. 

Now you need to add user and get the credentials, this can be done via **IAM console** > **Users** > click **add users**. The following are setting that you need to choose for this project:
- Since we're doing this using Boto3, in **AWS Access Type** section, choose **Programmatic Access**.
- In **Set Permissions** section, click **Attach existing policies directly**, choose **AdministratorAccess**. That permission policy will grant all access in AWS service.
- Can skip the **Add Tags** section.
- Don't forget to keep the **Access Key ID** and **Secret Access Key** safe for the next step.

**3. Set AWS *Key ID* & *Secret Access Key***

To be able to connect to AWS service use boto3, can use **client()** function that requires 2 keys:
- **aws_access_key_id**
- **aws_secret_access_key**

The **client()** function called can be found in `aws_config/create_boto_client.py`.

Those 2 keys created when you create new user in step 1, but if you forgot to keep it, can generate new keys on **IAM Console** > under **Access Management** tab on left screen, click **Users** > click **User Name** that you use > click **Security Credentials** tab > under **Access Keys** section, click **Create access key** button. Need to keep in mind, generating those new 2 keys will automatically deactivate the old one.

**4. Create Security Group**

Boto3 provides **create_security_group()** function to create **EC2 security group**, this function called in `aws_config/ec2.py`. That function requires following parameters:

| Parameter Name | Value Type | Description |
| --- | --- | --- |
| **GroupName** | string | Can type any random name for this |
| **Description** | string | Can type random brief description |
| **VpcId** | string | If you ***never*** create security group before, retrieve this **VpcId** on **VPC Console** > under **Virtual Private Cloud** tab on left screen, click **Your VPCs** > **VPC ID**. If you ***have*** created security group before, can also retrieve from **EC2 console** > under **Network & Security** tab on left screen, click **Security Groups** > **VPC ID** where *security group name* is default |

**5. Inbound Rule to Security Group**

After create EC2 security sroup, we need to add inbound rule to that. Boto3 provides **authorize_security_group_ingress()** function to set new inbound rule to our existing security group, this function called in `aws_config/ec2.py`. Need to set following parameters to make the func works:

| Parameter Name | Value Type | Description |
| --- | --- | --- |
| **IpProtocol** | string | Commonly **tcp** |
| **FromPort** | integer | Commonly **5432** |
| **ToPort** | integer | Commonly **5432** |
| **IpRanges** | list of dictionary with string value | Commonly **0.0.0.0/0**, basically this set to accept all IPs, not to set it to specific IP. You can change this to more specific IP. |

**6. Create DB Subnet Group**

Boto3 provides **create_db_subnet_group()** function to create the **DB subnet group**, this function called in `aws_config/rds.py`. Need to set following parameters to make the func works:

| Parameter Name | Value Type | Description |
| --- | --- | --- |
| **DBSubnetGroupName** | string | Can type any random name for this |
| **DBSubnetGroupDescription** | string | Can type random brief description |
| **SubnetIds** | list of string | If you ***never*** create DB subnet group before, retrieve this from **VPC Console** > under **Virtual Private Cloud** tab on left screen, click **Subnets** > use all Subnet IDs on list. If you ***have*** created DB subnet group before, can also retrieve this from **RDS console** > select **Subnet Groups** tab on left screen > **Subnet ID** |

**7. Setting DB Instance**

After create security group, add inbound rule, and create DB subnet group, now it's time to **create DB instance**. Boto3 provides **create_db_instance()** function to create DB instance, can see this func called in `aws_config/rds.py`. Parameters that needs to be set here includes:

| Parameter Name | Value Type |  Description |
| --- | --- | --- |
| **DBName** | string | The **name for the database** on your DB instance. If you don't provide a name, Amazon RDS doesn't create a database on the DB instance (except for Oracle and PostgreSQL).
| **DBInstanceIdentifier** | string | The **name for your DB instance**. Name your DB instances in the same way that you name your on-premises servers. |
| **DBInstanceClass** | string | The configuration for your DB instance. For example, a db.t3.small instance class has 2 GiB memory, 2 vCPUs, 1 virtual core, a variable ECU, and a moderate I/O capacity. For more information, see [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html) |
| **Engine** | string | The db engine. AWS provides Amzon Aurora, MariaDB, PostgreSQL, Oracle, & Microsoft SQL Server. |
| **DB engine version** | string | The version of database engine that you want to use. |
| **Port** | integer | The port that you want to access the DB instance through, e.g. **5432**. |
| **MasterUsername** | string | The name that you use as the master user name to log on to your DB instance with all database privileges. |
| **MasterUserPassword** | string | The password for your master user account. |
| **AllocatedStorage** | integer | The amount of storage to allocate for your DB instance (in gigabytes). |
| **MultiAZ** | boolean | Create a standby instance to create a passive secondary replica of your DB instance in another Availability Zone for failover support. |
| **StorageType** |  string | The storage type for your DB instance. For more information, see [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html#Concepts.Storage). |
| **PubliclyAccessible** | boolean | Set **True** if you want EC2 instances and devices outside of the VPC hosting the DB instance to connect to the DB instance. If set to **False**, Amazon RDS will not assign a public IP address to the DB instance, and no EC2 instance or devices outside of the VPC will be able to connect. |
| **VpcSecurityGroupIds** | list | If you are a **new** customer to AWS, Create new to create a new VPC security group. Otherwise, Choose **existing**, then choose from security groups that you previously created. When you choose Create new in the RDS console, a new security group is created. This new security group has an inbound rule that allows access to the DB instance from the IP address detected in your browser. For more information, see [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithSecurityGroups.html). |
| **DBSubnetGroupName** | string | This setting depends on the platform that you are on. If you are a **new** customer to AWS, choose default, which is the default DB subnet group that was created for your account. If you are **creating a DB instance on the earlier** E2-Classic platform, you might want your DB instance in a specific VPC. In this case, choose the DB subnet group that you created for that VPC.|

If you're using **free tier** AWS account, can see the limitation [here](https://aws.amazon.com/rds/free/). Kindly match the configuration with the limitation to avoid paying bills.

For more information regarding DB instance creation process, can check [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html).

**8. Get the DB Host & Port**

To check whether the DB has been successfully created or not, can visit **RDS Console** > select **Databases** tab on left screen. If you found **DB identifier** name that you just created, click that, and then on **Connectivity & Security** section, you can get the **endpoint** as your **host**, and **port**.