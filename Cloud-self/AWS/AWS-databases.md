<img width="751" height="423" alt="image" src="https://github.com/user-attachments/assets/5940562b-9757-4137-ba14-6891516018bc" />


# AWS Database Services - Complete Guide with Setup Instructions

## Overview
AWS offers a comprehensive suite of managed database services for different data models and use cases, eliminating the need to manage database infrastructure while providing high availability, scalability, and security.

---

## AWS Database Services Portfolio

### Relational Databases
- **Amazon RDS** - Managed relational database service
- **Amazon Aurora** - High-performance MySQL and PostgreSQL compatible
- **Amazon Redshift** - Data warehouse for analytics

### NoSQL Databases
- **Amazon DynamoDB** - Key-value and document database
- **Amazon DocumentDB** - MongoDB-compatible document database
- **Amazon Keyspaces** - Apache Cassandra-compatible

### In-Memory Databases
- **Amazon ElastiCache** - Redis and Memcached
- **Amazon MemoryDB for Redis** - Redis-compatible, durable

### Time-Series & Ledger
- **Amazon Timestream** - Time-series database
- **Amazon QLDB** - Ledger database (immutable transactions)

### Graph Database
- **Amazon Neptune** - Graph database for connected data

---

## 1. Amazon RDS (Relational Database Service)

### What is RDS?
Managed relational database service that supports multiple database engines, handling routine database tasks like provisioning, patching, backup, and scaling.

### Supported Database Engines
- **Amazon Aurora** (MySQL and PostgreSQL compatible)
- **MySQL**
- **PostgreSQL**
- **MariaDB**
- **Oracle Database**
- **Microsoft SQL Server**

### Key Features

**Automated Management:**
- Automatic software patching
- Automated backups (up to 35 days retention)
- Point-in-time recovery
- Automated failover
- OS and database maintenance

**High Availability:**
- **Multi-AZ deployment**: Synchronous replication to standby
- Automatic failover (1-2 minutes)
- Read replicas for read scaling (up to 15)

**Security:**
- VPC isolation
- Encryption at rest (KMS)
- Encryption in transit (SSL/TLS)
- IAM database authentication
- Network isolation with security groups

**Scalability:**
- Vertical scaling (change instance type)
- Horizontal scaling (read replicas)
- Storage auto-scaling
- Cross-region read replicas

**Backup and Recovery:**
- Automated daily backups
- Manual snapshots
- Restore to any point in time
- Cross-region snapshot copy

### RDS Instance Types

**General Purpose (db.t3, db.m5):**
- Balanced compute, memory, network
- Burstable performance (T3)
- Use cases: Small to medium databases

**Memory Optimized (db.r5, db.x2):**
- High memory-to-CPU ratio
- Use cases: In-memory databases, caching

**Burstable Performance (db.t3, db.t4g):**
- Baseline performance with burst capability
- Cost-effective for variable workloads

### RDS Storage Types

**General Purpose SSD (gp3, gp2):**
- 3 IOPS per GB (gp2)
- Configurable IOPS and throughput (gp3)
- Size: 20 GB to 64 TB
- Best for: Most workloads

**Provisioned IOPS SSD (io1, io2):**
- High performance
- Up to 256,000 IOPS
- Size: 100 GB to 64 TB
- Best for: I/O intensive workloads

**Magnetic (Standard):**
- Legacy, not recommended
- Use cases: Backward compatibility only

---

## Setup Guide: Amazon RDS (MySQL)

### Prerequisites
- AWS Account
- AWS CLI installed (optional)
- VPC with subnets in multiple AZs

### Step 1: Create RDS MySQL Database (Console)

**Navigate to RDS:**
```
AWS Console → Services → RDS → Create database
```

**Choose Database Creation Method:**
- Select "Standard create" for full control
- Or "Easy create" for quick setup with defaults

**Engine Options:**
```yaml
Engine type: MySQL
Edition: MySQL Community
Engine version: 8.0.35 (or latest)
```

**Templates:**
- **Production**: Multi-AZ, high IOPS
- **Dev/Test**: Single instance, balanced
- **Free Tier**: Limited resources, single AZ

**Settings:**
```yaml
DB instance identifier: my-mysql-db
Master username: admin
Master password: YourSecurePassword123!
Confirm password: YourSecurePassword123!
```

**Instance Configuration:**
```yaml
DB instance class: db.t3.micro (Free Tier eligible)
# For production:
# DB instance class: db.m5.large or higher

vCPUs: 2
Memory: 1 GB (t3.micro)
```

**Storage:**
```yaml
Storage type: General Purpose SSD (gp3)
Allocated storage: 20 GB
Storage autoscaling: Enable
Maximum storage threshold: 1000 GB
```

**Availability & Durability:**
```yaml
Multi-AZ deployment: 
  - Enable for production (creates standby in another AZ)
  - Disable for dev/test

# Multi-AZ provides:
# - Automatic failover
# - Synchronous replication
# - Higher availability
```

**Connectivity:**
```yaml
Virtual Private Cloud (VPC): Select your VPC
Subnet group: Default or custom
Public access: No (recommended for production)
VPC security group: Create new or select existing
Availability Zone: No preference (or specific AZ)
```

**Database Authentication:**
```yaml
Options:
  ☑ Password authentication
  ☐ Password and IAM database authentication
  ☐ Password and Kerberos authentication
```

**Additional Configuration:**

**Database Options:**
```yaml
Initial database name: mydatabase
DB parameter group: default.mysql8.0
Option group: default:mysql-8-0
```

**Backup:**
```yaml
Backup retention period: 7 days (1-35 days)
Backup window: No preference or specific time
☑ Copy tags to snapshots
```

**Encryption:**
```yaml
☑ Enable encryption
Encryption key: (default) aws/rds or custom KMS key
```

**Monitoring:**
```yaml
☑ Enable Enhanced Monitoring
Granularity: 60 seconds
Monitoring Role: Create new role or use existing
☑ Enable Performance Insights
Retention: 7 days (free) or longer (paid)
```

**Maintenance:**
```yaml
☑ Enable auto minor version upgrade
Maintenance window: No preference or specific time
☐ Enable deletion protection (enable for production)
```

**Click "Create database"**

**Wait for Creation:**
- Status will change from "Creating" to "Available"
- Takes 5-15 minutes
- Endpoint will be displayed once available

### Step 2: Configure Security Group

**Locate Security Group:**
```
RDS Console → Your DB instance → Connectivity & security → 
  VPC security groups → Click security group ID
```

**Add Inbound Rule:**
```yaml
Type: MySQL/Aurora
Protocol: TCP
Port: 3306
Source: 
  - Custom: Your application security group ID
  - Or: Your IP (for testing only)
  - Or: VPC CIDR block
Description: Allow MySQL access from app tier
```

**Click "Save rules"**

### Step 3: Connect to RDS MySQL

**Get Connection Details:**
```
RDS Console → Your DB instance → Connectivity & security
Copy: Endpoint and Port
```

**Endpoint format:**
```
my-mysql-db.c1234567890.us-east-1.rds.amazonaws.com:3306
```

**Connect from EC2 Instance (same VPC):**

**Install MySQL Client:**
```bash
# Amazon Linux 2
sudo yum install mysql -y

# Ubuntu
sudo apt-get update
sudo apt-get install mysql-client -y
```

**Connect:**
```bash
mysql -h my-mysql-db.c1234567890.us-east-1.rds.amazonaws.com \
      -P 3306 \
      -u admin \
      -p

# Enter password when prompted
```

**Test Connection:**
```sql
-- Show databases
SHOW DATABASES;

-- Create a test database
CREATE DATABASE testdb;

-- Use the database
USE testdb;

-- Create a test table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (username, email) 
VALUES ('john_doe', 'john@example.com');

-- Query data
SELECT * FROM users;
```

### Step 4: Setup Using AWS CLI

**Create DB Instance:**
```bash
aws rds create-db-instance \
    --db-instance-identifier my-mysql-db \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --engine-version 8.0.35 \
    --master-username admin \
    --master-user-password YourSecurePassword123! \
    --allocated-storage 20 \
    --storage-type gp3 \
    --vpc-security-group-ids sg-0123456789abcdef0 \
    --db-subnet-group-name default \
    --backup-retention-period 7 \
    --preferred-backup-window "03:00-04:00" \
    --preferred-maintenance-window "mon:04:00-mon:05:00" \
    --no-multi-az \
    --storage-encrypted \
    --enable-cloudwatch-logs-exports '["error","general","slowquery"]' \
    --tags Key=Environment,Value=Development
```

**Check Status:**
```bash
aws rds describe-db-instances \
    --db-instance-identifier my-mysql-db \
    --query 'DBInstances[0].DBInstanceStatus'
```

**Get Endpoint:**
```bash
aws rds describe-db-instances \
    --db-instance-identifier my-mysql-db \
    --query 'DBInstances[0].Endpoint.Address' \
    --output text
```

### Step 5: Application Connection

**Python (using pymysql):**
```python
import pymysql

# Connection configuration
connection = pymysql.connect(
    host='my-mysql-db.c1234567890.us-east-1.rds.amazonaws.com',
    user='admin',
    password='YourSecurePassword123!',
    database='mydatabase',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # Create table
        sql = """CREATE TABLE IF NOT EXISTS products (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100),
                    price DECIMAL(10,2)
                )"""
        cursor.execute(sql)
        
        # Insert data
        sql = "INSERT INTO products (name, price) VALUES (%s, %s)"
        cursor.execute(sql, ('Laptop', 999.99))
        connection.commit()
        
        # Query data
        sql = "SELECT * FROM products"
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
finally:
    connection.close()
```

**Node.js (using mysql2):**
```javascript
const mysql = require('mysql2');

const connection = mysql.createConnection({
  host: 'my-mysql-db.c1234567890.us-east-1.rds.amazonaws.com',
  user: 'admin',
  password: 'YourSecurePassword123!',
  database: 'mydatabase',
  port: 3306
});

connection.connect((err) => {
  if (err) {
    console.error('Error connecting: ' + err.stack);
    return;
  }
  console.log('Connected as id ' + connection.threadId);
});

// Query
connection.query('SELECT * FROM products', (err, results) => {
  if (err) throw err;
  console.log(results);
});

connection.end();
```

### Step 6: Create Read Replica (Optional)

**Console Method:**
```
RDS Console → Select DB instance → Actions → Create read replica

Settings:
- Read replica identifier: my-mysql-db-replica
- Destination region: Same or different region
- Instance specifications: Same or different
- Public accessibility: No
- Create
```

**CLI Method:**
```bash
aws rds create-db-instance-read-replica \
    --db-instance-identifier my-mysql-db-replica \
    --source-db-instance-identifier my-mysql-db \
    --db-instance-class db.t3.micro \
    --publicly-accessible false
```

**Connect to Read Replica:**
```bash
# Use read replica endpoint for read queries
mysql -h my-mysql-db-replica.c1234567890.us-east-1.rds.amazonaws.com \
      -u admin -p
```

### Step 7: Enable Multi-AZ (Production)

**For Existing Instance:**
```
RDS Console → Select DB instance → Modify

Availability & durability:
☑ Create a standby instance

Apply: Immediately or during maintenance window
```

**CLI Method:**
```bash
aws rds modify-db-instance \
    --db-instance-identifier my-mysql-db \
    --multi-az \
    --apply-immediately
```

### Step 8: Backup and Restore

**Create Manual Snapshot:**
```bash
aws rds create-db-snapshot \
    --db-instance-identifier my-mysql-db \
    --db-snapshot-identifier my-mysql-backup-$(date +%Y%m%d)
```

**Restore from Snapshot:**
```bash
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier my-mysql-db-restored \
    --db-snapshot-identifier my-mysql-backup-20250102
```

**Point-in-Time Restore:**
```bash
aws rds restore-db-instance-to-point-in-time \
    --source-db-instance-identifier my-mysql-db \
    --target-db-instance-identifier my-mysql-db-pitr \
    --restore-time 2025-01-02T10:30:00Z
```

### Step 9: Monitoring and Maintenance

**View Metrics in CloudWatch:**
```
CloudWatch Console → Metrics → RDS

Key Metrics:
- CPUUtilization
- DatabaseConnections
- FreeableMemory
- ReadIOPS / WriteIOPS
- ReadLatency / WriteLatency
- FreeStorageSpace
```

**Enhanced Monitoring:**
- Real-time OS metrics
- Process list
- CPU usage per core
- Memory usage breakdown

**Performance Insights:**
- Query performance analysis
- Wait events
- Top SQL queries
- Database load

**Set Up Alarms:**
```bash
aws cloudwatch put-metric-alarm \
    --alarm-name rds-high-cpu \
    --alarm-description "Alert when CPU exceeds 80%" \
    --metric-name CPUUtilization \
    --namespace AWS/RDS \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2 \
    --dimensions Name=DBInstanceIdentifier,Value=my-mysql-db \
    --alarm-actions arn:aws:sns:us-east-1:123456789012:my-sns-topic
```

---

## 2. Amazon Aurora

### What is Aurora?
MySQL and PostgreSQL-compatible relational database built for the cloud, offering up to 5x throughput of MySQL and 3x throughput of PostgreSQL.

### Key Features

**Performance:**
- 5x faster than standard MySQL
- 3x faster than standard PostgreSQL
- Up to 128 TB storage auto-scaling
- Up to 15 read replicas

**High Availability:**
- 6 copies of data across 3 AZs
- Continuous backup to S3
- Instant crash recovery
- Automatic failover (< 30 seconds)

**Aurora Serverless:**
- Auto-scaling based on demand
- Pay per second for compute
- No capacity planning needed
- Automatic pause during inactivity

**Aurora Global Database:**
- Cross-region replication (< 1 second)
- Fast regional failover
- Read replicas in up to 5 regions
- Disaster recovery

### Aurora Architecture

```
Aurora Cluster:
┌─────────────────────────────────────┐
│  Primary Instance (Read/Write)      │
│  ↓                                   │
│  Storage Layer (6 copies, 3 AZs)    │
│  ↑                                   │
│  Read Replica 1, 2, ... 15          │
└─────────────────────────────────────┘
```

---

## Setup Guide: Amazon Aurora MySQL

### Step 1: Create Aurora Cluster

**Console Method:**
```
RDS Console → Create database

Engine options:
- Engine type: Amazon Aurora
- Edition: Amazon Aurora MySQL-Compatible Edition
- Capacity type: Provisioned (or Serverless v2)
- Engine version: Aurora MySQL 3.04.0 (compatible with MySQL 8.0.28)

Templates: Production

Settings:
- DB cluster identifier: my-aurora-cluster
- Master username: admin
- Master password: YourSecurePassword123!

DB instance class:
- Memory optimized: db.r6g.large
- Or Burstable: db.t4g.medium

Multi-AZ deployment:
☑ Create an Aurora Replica in a different AZ

Connectivity:
- VPC: Select your VPC
- Public access: No
- VPC security group: Select or create

Database authentication:
☑ Password authentication

Additional configuration:
- Initial database name: myauroradb
- Backup retention: 7 days
- Encryption: Enable
- Enhanced monitoring: Enable
- Performance Insights: Enable

Create database
```

### Step 2: Add Aurora Read Replicas

**Console:**
```
RDS Console → Databases → Select cluster → 
  Actions → Add reader

Reader settings:
- DB instance identifier: my-aurora-cluster-reader-1
- Instance class: db.t4g.medium
- Availability zone: Different from primary

Add reader
```

**CLI:**
```bash
aws rds create-db-instance \
    --db-instance-identifier my-aurora-cluster-reader-1 \
    --db-instance-class db.t4g.medium \
    --engine aurora-mysql \
    --db-cluster-identifier my-aurora-cluster
```

### Step 3: Connect to Aurora

**Primary Endpoint (Read/Write):**
```bash
mysql -h my-aurora-cluster.cluster-c1234567890.us-east-1.rds.amazonaws.com \
      -u admin -p
```

**Reader Endpoint (Read-Only):**
```bash
mysql -h my-aurora-cluster.cluster-ro-c1234567890.us-east-1.rds.amazonaws.com \
      -u admin -p
```

**Application Configuration:**
```python
# Write operations
write_connection = pymysql.connect(
    host='my-aurora-cluster.cluster-c1234567890.us-east-1.rds.amazonaws.com',
    user='admin',
    password='password',
    database='myauroradb'
)

# Read operations (load balanced across readers)
read_connection = pymysql.connect(
    host='my-aurora-cluster.cluster-ro-c1234567890.us-east-1.rds.amazonaws.com',
    user='admin',
    password='password',
    database='myauroradb'
)
```

---

## 3. Amazon DynamoDB

### What is DynamoDB?
Fully managed NoSQL database service providing single-digit millisecond performance at any scale with built-in security, backup, and in-memory caching.

### Key Features

**Performance:**
- Single-digit millisecond latency
- Trillions of requests per day
- Support for 20+ million requests per second

**Scalability:**
- Automatic horizontal scaling
- No server management
- Global tables (multi-region replication)

**Flexibility:**
- Key-value and document data models
- Flexible schema
- Support for complex data types

**Built-in Features:**
- DynamoDB Streams (change data capture)
- Global secondary indexes (GSI)
- Local secondary indexes (LSI)
- Point-in-time recovery
- On-demand backup and restore
- Encryption at rest

### Data Model

**Core Components:**
- **Table**: Collection of items
- **Item**: Collection of attributes (like a row)
- **Attribute**: Fundamental data element (like a column)
- **Primary Key**: Uniquely identifies each item
  - Partition key (hash key)
  - Partition key + Sort key (composite key)

### Capacity Modes

**Provisioned:**
- Specify read/write capacity units (RCU/WCU)
- Predictable traffic
- Auto-scaling available
- Lower cost for consistent workload

**On-Demand:**
- Pay per request
- Automatic scaling
- Unpredictable traffic
- Higher per-request cost

---

## Setup Guide: Amazon DynamoDB

### Step 1: Create DynamoDB Table

**Console Method:**
```
DynamoDB Console → Tables → Create table

Table details:
- Table name: Users
- Partition key: userId (String)
- Sort key: timestamp (Number) [Optional]

Table settings:
- Customize settings
- Table class: DynamoDB Standard
- Capacity mode: On-demand (or Provisioned)

If Provisioned:
- Read capacity: 5 RCU
- Write capacity: 5 WCU
- ☑ Enable auto-scaling

Encryption at rest:
- Owned by Amazon DynamoDB (default)
- Or AWS managed key
- Or Customer managed key

Tags: [Optional]
Key: Environment, Value: Development

Create table
```

### Step 2: Create Table with CLI

```bash
aws dynamodb create-table \
    --table-name Users \
    --attribute-definitions \
        AttributeName=userId,AttributeType=S \
        AttributeName=timestamp,AttributeType=N \
    --key-schema \
        AttributeName=userId,KeyType=HASH \
        AttributeName=timestamp,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --tags Key=Environment,Value=Development
```

**With Provisioned Capacity:**
```bash
aws dynamodb create-table \
    --table-name Users \
    --attribute-definitions \
        AttributeName=userId,AttributeType=S \
    --key-schema \
        AttributeName=userId,KeyType=HASH \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --stream-specification \
        StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES
```

### Step 3: Add Items

**Console:**
```
DynamoDB Console → Tables → Users → 
  Explore table items → Create item

Attributes:
userId (String): user123
timestamp (Number): 1704211200
name (String): John Doe
email (String): john@example.com
age (Number): 30
status (String): active

Create item
```

**CLI - Put Item:**
```bash
aws dynamodb put-item \
    --table-name Users \
    --item '{
        "userId": {"S": "user123"},
        "timestamp": {"N": "1704211200"},
        "name": {"S": "John Doe"},
        "email": {"S": "john@example.com"},
        "age": {"N": "30"},
        "status": {"S": "active"}
    }'
```

**Batch Write:**
```bash
aws dynamodb batch-write-item \
    --request-items file://batch-items.json
```

**batch-items.json:**
```json
{
  "Users": [
    {
      "PutRequest": {
        "Item": {
          "userId": {"S": "user124"},
          "timestamp": {"N": "1704211201"},
          "name": {"S": "Jane Smith"},
          "email": {"S": "jane@example.com"}
        }
      }
    },
    {
      "PutRequest": {
        "Item": {
          "userId": {"S": "user125"},
          "timestamp": {"N": "1704211202"},
          "name": {"S": "Bob Johnson"},
          "email": {"S": "bob@example.com"}
        }
      }
    }
  ]
}
```

### Step 4: Query and Scan

**Get Item by Primary Key:**
```bash
aws dynamodb get-item \
    --table-name Users \
    --key '{
        "userId": {"S": "user123"},
        "timestamp": {"N": "1704211200"}
    }'
```

**Query Items:**
```bash
# Query all items with specific partition key
aws dynamodb query \
    --table-name Users \
    --key-condition-expression "userId = :uid" \
    --expression-attribute-values '{
        ":uid": {"S": "user123"}
    }'

# Query with sort key condition
aws dynamodb query \
    --table-name Users \
    --key-condition-expression "userId = :uid AND #ts > :start" \
    --expression-attribute-names '{
        "#ts": "timestamp"
    }' \
    --expression-attribute-values '{
        ":uid": {"S": "user123"},
        ":start": {"N": "1704211000"}
    }'
```

**Scan Table:**
```bash
# Scan with filter
aws dynamodb scan \
    --table-name Users \
    --filter-expression "age > :min_age" \
    --expression-attribute-values '{
        ":min_age": {"N": "25"}
    }'
```

### Step 5: Update Items

```bash
aws dynamodb update-item \
    --table-name Users \
    --key '{
        "userId": {"S": "user123"},
        "timestamp": {"N": "1704211200"}
    }' \
    --update-expression "SET #status = :new_status, age = age + :inc" \
    --expression-attribute-names '{
        "#status": "status"
    }' \
    --expression-attribute-values '{
        ":new_status": {"S": "inactive"},
        ":inc": {"N": "1"}
    }' \
    --return-values ALL_NEW
```

### Step 6: Delete Items

```bash
aws dynamodb delete-item \
    --table-name Users \
    --key '{
        "userId": {"S": "user123"},
        "timestamp": {"N": "1704211200"}
    }'
```

### Step 7: Create Global Secondary Index (GSI)

**Console:**
```
DynamoDB Console → Tables → Users → Indexes → Create index

Index details:
- Partition key: email (String)
- Sort key: [Optional]
- Index name: email-index
- Attribute projections: All

Create index
```

**CLI:**
```bash
aws dynamodb update-table \
    --table-name Users \
    --attribute-definitions \
        AttributeName=email,AttributeType=S \
    --global-secondary-index-updates '[
        {
            "Create": {
                "IndexName": "email-index",
                "KeySchema": [
                    {"AttributeName": "email", "KeyType": "HASH"}
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            }
        }
    ]'
```

**Query GSI:**
```bash
aws dynamodb query \
    --table-name Users \
    --index-name email-index \
    --key-condition-expression "email = :email" \
    --expression-attribute-values '{
        ":email": {"S": "john@example.com"}
    }'
```

### Step 8: Application Integration

**Python (boto3):**
```python
import boto3
from decimal import Decimal

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Users')

# Put item
response = table.put_item(
    Item={
        'userId': 'user126',
        'timestamp': 1704211203,
        'name': 'Alice Brown',
        'email': 'alice@example.com',
        'age': 28,
        'preferences': {
            'theme': 'dark',
            'notifications': True
        }
    }
)

# Get item
response = table.get_item(
    Key={
        'userId': 'user126',
        'timestamp': 1704211203
    }
)
item = response.get('Item')
print(item)

# Query
response = table.query(
    KeyConditionExpression='userId = :uid',
    ExpressionAttributeValues={
        ':uid': 'user126'
    }
)
items = response['Items']

# Update
response = table.update_item(
    Key={
        'userId': 'user126',
        'timestamp': 1704211203
    },
    UpdateExpression='SET age = :new_age, #s = :status',
    ExpressionAttributeNames={
        '#s': 'status'
    },
    ExpressionAttributeValues={
        ':new_age': 29,
        ':status': 'active'
    },
    ReturnValues='ALL_NEW'
)

# Delete
response = table.delete_item(
    Key={
        'userId': 'user126',
        'timestamp': 1704211203
    }
)

# Batch operations
with table.batch_writer() as batch:
    for i in range(100):
        batch.put_item(
            Item={
                'userId': f'user{i}',
                'timestamp': 1704211200 + i,
                'name': f'User {i}',
                'email': f'user{i}@example.com'
            }
        )
```

**Node.js (AWS SDK v3):**
```javascript
const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const {
  DynamoDBDocumentClient,
  PutCommand,
  GetCommand,
  QueryCommand,
  UpdateCommand,
  DeleteCommand
} = require('@aws-sdk/lib-dynamodb');

const client = new DynamoDBClient({ region: 'us-east-1' });
const docClient = DynamoDBDocumentClient.from(client);

// Put item
const putItem = async () => {
  const command = new PutCommand({
    TableName: 'Users',
    Item: {
      userId: 'user127',
      timestamp: 1704211204,
      name: 'Charlie Davis',
      email: 'charlie@example.com',
      age: 35
    }
  });
  
  const response = await docClient.send(command);
  console.log(response);
};

// Get item
const getItem = async () => {
  const command = new GetCommand({
    TableName: 'Users',
    Key: {
      userId: 'user127',
      timestamp: 1704211204
    }
  });
  
  const response = await docClient.send(command);
  console.log(response.Item);
};

// Query
const queryItems = async () => {
  const command = new QueryCommand({
    TableName: 'Users',
    KeyConditionExpression: 'userId = :uid',
    ExpressionAttributeValues: {
      ':uid': 'user127'
    }
  });
  
  const response = await docClient.send(command);
  console.log(response.Items);
};

// Update
const updateItem = async () => {
  const command = new UpdateCommand({
    TableName: 'Users',
    Key: {
      userId: 'user127',
      timestamp: 1704211204
    },
    UpdateExpression: 'SET age = :newAge',
    ExpressionAttributeValues: {
      ':newAge': 36
    },
    ReturnValues: 'ALL_NEW'
  });
  
  const response = await docClient.send(command);
  console.log(response.Attributes);
};

// Delete
const deleteItem = async () => {
  const command = new DeleteCommand({
    TableName: 'Users',
    Key: {
      userId: 'user127',
      timestamp: 1704211204
    }
  });
  
  const response = await docClient.send(command);
  console.log(response);
};
```

### Step 9
