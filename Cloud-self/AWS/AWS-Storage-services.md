<img width="1045" height="479" alt="image" src="https://github.com/user-attachments/assets/6fcf536e-d019-4e1c-b48e-38d5bc7badaa" />


<img width="1068" height="551" alt="image" src="https://github.com/user-attachments/assets/0f99c5db-6a1e-4b94-b6c1-08c14d46de65" />


<img width="1097" height="479" alt="image" src="https://github.com/user-attachments/assets/0f2923f4-f849-4051-a335-2a157c070586" />

<img width="808" height="531" alt="image" src="https://github.com/user-attachments/assets/b5686a74-54df-49e9-89f6-5c29a4d6a2d7" />


# AWS Storage Services - Complete Guide

## Overview
AWS provides a comprehensive suite of storage services designed for different use cases, from object storage to file systems, block storage, and data transfer solutions.

---

## AWS Storage Services Portfolio

### Object Storage
- **Amazon S3** - Scalable object storage
- **Amazon S3 Glacier** - Long-term archival storage

### Block Storage
- **Amazon EBS** - EC2 block storage volumes
- **Amazon EC2 Instance Store** - Temporary block storage

### File Storage
- **Amazon EFS** - Elastic file system (Linux)
- **Amazon FSx** - Managed file systems (Windows, Lustre, NetApp, OpenZFS)

### Data Transfer & Migration
- **AWS Storage Gateway** - Hybrid cloud storage
- **AWS DataSync** - Automated data transfer
- **AWS Transfer Family** - SFTP, FTPS, FTP file transfers
- **AWS Snow Family** - Physical data transport

### Backup & Disaster Recovery
- **AWS Backup** - Centralized backup service
- **AWS Elastic Disaster Recovery** - Application recovery service

---

## 1. Amazon S3 (Simple Storage Service)

### What is S3?
Amazon S3 is an object storage service offering industry-leading scalability, data availability, security, and performance for storing and retrieving any amount of data from anywhere.

### Key Concepts

**Buckets:**
- Container for objects
- Globally unique name (across all AWS accounts)
- Region-specific
- Unlimited number of objects per bucket

**Objects:**
- Files stored in S3
- Consists of: data, metadata, key (filename)
- Size: 0 bytes to 5 TB
- Key = Full path (e.g., `folder/subfolder/file.txt`)

**Storage Classes:**
Different tiers optimized for different access patterns and cost

### S3 Storage Classes

**S3 Standard:**
- Frequently accessed data
- Low latency, high throughput
- 99.99% availability
- Use: Active data, websites, content distribution

**S3 Intelligent-Tiering:**
- Automatic cost optimization
- Moves data between access tiers based on usage
- No retrieval fees
- Small monthly monitoring fee
- Use: Unknown or changing access patterns

**S3 Standard-IA (Infrequent Access):**
- Less frequently accessed data
- Lower storage cost, retrieval fee applies
- 99.9% availability
- Use: Backups, disaster recovery

**S3 One Zone-IA:**
- Single AZ storage
- 20% less cost than Standard-IA
- 99.5% availability
- Use: Secondary backup copies, recreatable data

**S3 Glacier Instant Retrieval:**
- Archive data with instant access
- Millisecond retrieval
- Minimum 90-day storage duration
- Use: Medical images, news archives

**S3 Glacier Flexible Retrieval (formerly Glacier):**
- Archive data
- Retrieval: Minutes to hours
- Minimum 90-day storage duration
- Use: Long-term backups, compliance archives

**S3 Glacier Deep Archive:**
- Lowest cost storage
- Retrieval: 12-48 hours
- Minimum 180-day storage duration
- Use: Data retained for 7-10 years, compliance

**S3 Outposts:**
- On-premises S3 storage
- Use: Local data residency requirements

### S3 Features

**Versioning:**
- Keep multiple versions of objects
- Protection against accidental deletion
- Easy rollback to previous versions

**Replication:**
- **Cross-Region Replication (CRR)**: Replicate across regions
- **Same-Region Replication (SRR)**: Replicate within region
- Use: Compliance, lower latency, disaster recovery

**Lifecycle Policies:**
- Automatically transition objects between storage classes
- Automatically delete objects after specified time
- Cost optimization

**Encryption:**
- **At Rest**: SSE-S3, SSE-KMS, SSE-C, Client-side
- **In Transit**: SSL/TLS (HTTPS)

**Access Control:**
- Bucket policies
- IAM policies
- Access Control Lists (ACLs)
- Pre-signed URLs
- S3 Access Points

**Security Features:**
- Block Public Access (BPA)
- S3 Object Lock (WORM - Write Once Read Many)
- MFA Delete
- Access Logging
- CloudTrail integration

**Performance:**
- 3,500 PUT/COPY/POST/DELETE requests per second per prefix
- 5,500 GET/HEAD requests per second per prefix
- Multi-part upload (files > 100 MB)
- Transfer Acceleration (CloudFront edge locations)

---

## Setup Guide: Amazon S3

### Step 1: Create S3 Bucket

**Console Method:**
```
S3 Console → Buckets → Create bucket

General configuration:
- Bucket name: my-unique-bucket-name-12345
  (must be globally unique, lowercase, no underscores)
- AWS Region: US East (N. Virginia) us-east-1

Object Ownership:
- ACLs disabled (recommended)
  Bucket owner enforced

Block Public Access settings:
☑ Block all public access (recommended for most use cases)

Bucket Versioning:
- Disable (or Enable for version control)

Tags: [Optional]
Key: Environment, Value: Development

Default encryption:
- Server-side encryption: Enable
- Encryption type: 
  • Amazon S3-managed keys (SSE-S3) [Default]
  • AWS Key Management Service keys (SSE-KMS)

Advanced settings:
Object Lock: Disable (unless WORM compliance needed)

Create bucket
```

**CLI Method:**
```bash
# Create bucket
aws s3 mb s3://my-unique-bucket-name-12345 --region us-east-1

# Create bucket with encryption
aws s3api create-bucket \
    --bucket my-unique-bucket-name-12345 \
    --region us-east-1 \
    --create-bucket-configuration LocationConstraint=us-east-1 \
    --object-ownership BucketOwnerEnforced

# Enable versioning
aws s3api put-bucket-versioning \
    --bucket my-unique-bucket-name-12345 \
    --versioning-configuration Status=Enabled

# Enable default encryption
aws s3api put-bucket-encryption \
    --bucket my-unique-bucket-name-12345 \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            },
            "BucketKeyEnabled": true
        }]
    }'
```

### Step 2: Upload Objects

**Console:**
```
S3 Console → Buckets → my-unique-bucket-name-12345 → Upload

Add files or Add folder

Destination:
s3://my-unique-bucket-name-12345/

Permissions:
- Predefined ACLs: None
- Access control list (ACL): [Default]

Properties:
Storage class: Standard (or choose different class)

Server-side encryption: 
- Specify encryption settings for individual objects (optional)

Tags: [Optional]

Upload
```

**CLI Method:**
```bash
# Upload single file
aws s3 cp myfile.txt s3://my-unique-bucket-name-12345/

# Upload with storage class
aws s3 cp myfile.txt s3://my-unique-bucket-name-12345/ \
    --storage-class INTELLIGENT_TIERING

# Upload entire directory
aws s3 cp myfolder/ s3://my-unique-bucket-name-12345/myfolder/ --recursive

# Sync directory (only uploads new/changed files)
aws s3 sync myfolder/ s3://my-unique-bucket-name-12345/myfolder/

# Upload with metadata
aws s3 cp myfile.txt s3://my-unique-bucket-name-12345/ \
    --metadata "key1=value1,key2=value2"

# Upload with server-side encryption
aws s3 cp myfile.txt s3://my-unique-bucket-name-12345/ \
    --server-side-encryption AES256
```

### Step 3: Download Objects

**CLI:**
```bash
# Download single file
aws s3 cp s3://my-unique-bucket-name-12345/myfile.txt ./

# Download entire folder
aws s3 cp s3://my-unique-bucket-name-12345/myfolder/ ./myfolder/ --recursive

# Sync from S3 to local
aws s3 sync s3://my-unique-bucket-name-12345/myfolder/ ./myfolder/
```

### Step 4: Set Bucket Policy

**Example Bucket Policy (Read-Only Public Access):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-unique-bucket-name-12345/*"
    }
  ]
}
```

**Apply Policy:**
```bash
aws s3api put-bucket-policy \
    --bucket my-unique-bucket-name-12345 \
    --policy file://bucket-policy.json
```

**Example: Allow Access from Specific VPC Endpoint:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Access-from-specific-VPCE",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-unique-bucket-name-12345",
        "arn:aws:s3:::my-unique-bucket-name-12345/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:SourceVpce": "vpce-1234567890abcdef0"
        }
      }
    }
  ]
}
```

### Step 5: Enable S3 Versioning

**Console:**
```
S3 Console → Buckets → my-unique-bucket-name-12345 → 
  Properties → Bucket Versioning → Edit

Bucket Versioning: Enable

Save changes
```

**CLI:**
```bash
aws s3api put-bucket-versioning \
    --bucket my-unique-bucket-name-12345 \
    --versioning-configuration Status=Enabled
```

**Work with Versions:**
```bash
# List all versions
aws s3api list-object-versions \
    --bucket my-unique-bucket-name-12345

# Download specific version
aws s3api get-object \
    --bucket my-unique-bucket-name-12345 \
    --key myfile.txt \
    --version-id "version-id-here" \
    myfile-v1.txt

# Delete specific version
aws s3api delete-object \
    --bucket my-unique-bucket-name-12345 \
    --key myfile.txt \
    --version-id "version-id-here"
```

### Step 6: Configure Lifecycle Policies

**Console:**
```
S3 Console → Buckets → my-unique-bucket-name-12345 → 
  Management → Create lifecycle rule

Lifecycle rule configuration:
- Lifecycle rule name: transition-to-glacier
- Choose rule scope: Apply to all objects in bucket

Lifecycle rule actions:
☑ Transition current versions of objects between storage classes
☑ Transition previous versions of objects between storage classes
☑ Expire current versions of objects
☑ Permanently delete previous versions of objects
☑ Delete expired object delete markers

Transition current versions:
- Days after object creation: 30
- Storage class transition: Standard-IA

- Days after object creation: 90
- Storage class transition: Glacier Flexible Retrieval

Expire current versions:
- Days after object creation: 365

Transition previous versions:
- Days after objects become previous versions: 30
- Storage class transition: Glacier Flexible Retrieval

Delete previous versions:
- Days after objects become previous versions: 90

Create rule
```

**CLI - Lifecycle Policy JSON:**
```json
{
  "Rules": [
    {
      "Id": "transition-to-glacier",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ],
      "NoncurrentVersionTransitions": [
        {
          "NoncurrentDays": 30,
          "StorageClass": "GLACIER"
        }
      ],
      "NoncurrentVersionExpiration": {
        "NoncurrentDays": 90
      },
      "Expiration": {
        "Days": 365
      }
    }
  ]
}
```

**Apply Lifecycle Policy:**
```bash
aws s3api put-bucket-lifecycle-configuration \
    --bucket my-unique-bucket-name-12345 \
    --lifecycle-configuration file://lifecycle-policy.json
```

### Step 7: Enable Cross-Region Replication

**Prerequisites:**
- Versioning enabled on source and destination buckets
- IAM role with replication permissions

**Console:**
```
S3 Console → Buckets → my-unique-bucket-name-12345 → 
  Management → Replication rules → Create replication rule

Replication rule configuration:
- Rule name: replicate-to-west
- Status: Enabled
- Priority: 1

Source:
☑ Apply to all objects in the bucket

Destination:
- Choose a bucket in this account
- Bucket name: my-replica-bucket-west
  (in different region, e.g., us-west-2)

IAM role:
- Create new role (S3 will create it automatically)

Encryption:
☑ Replicate objects encrypted with AWS KMS

Additional replication options:
☑ Replication Time Control (RTC) [Optional - guaranteed 15 min]
☑ Replication metrics and notifications
☑ Delete marker replication

Save
```

**CLI:**
```bash
# Create replication configuration
aws s3api put-bucket-replication \
    --bucket my-unique-bucket-name-12345 \
    --replication-configuration file://replication-config.json
```

**replication-config.json:**
```json
{
  "Role": "arn:aws:iam::123456789012:role/s3-replication-role",
  "Rules": [
    {
      "Status": "Enabled",
      "Priority": 1,
      "DeleteMarkerReplication": {
        "Status": "Enabled"
      },
      "Filter": {},
      "Destination": {
        "Bucket": "arn:aws:s3:::my-replica-bucket-west",
        "ReplicationTime": {
          "Status": "Enabled",
          "Time": {
            "Minutes": 15
          }
        },
        "Metrics": {
          "Status": "Enabled",
          "EventThreshold": {
            "Minutes": 15
          }
        }
      }
    }
  ]
}
```

### Step 8: Enable S3 Event Notifications

**Console:**
```
S3 Console → Buckets → my-unique-bucket-name-12345 → 
  Properties → Event notifications → Create event notification

General configuration:
- Event name: notify-on-upload
- Prefix: uploads/ [Optional - filter by folder]
- Suffix: .jpg [Optional - filter by extension]

Event types:
☑ All object create events
  Or select specific:
  • s3:ObjectCreated:Put
  • s3:ObjectCreated:Post
  • s3:ObjectCreated:Copy
  • s3:ObjectCreated:CompleteMultipartUpload

Destination:
- Choose: Lambda function / SNS topic / SQS queue
- Select: my-processing-lambda

Save changes
```

**CLI:**
```bash
aws s3api put-bucket-notification-configuration \
    --bucket my-unique-bucket-name-12345 \
    --notification-configuration file://notification-config.json
```

**notification-config.json:**
```json
{
  "LambdaFunctionConfigurations": [
    {
      "Id": "notify-on-upload",
      "LambdaFunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processing-lambda",
      "Events": ["s3:ObjectCreated:*"],
      "Filter": {
        "Key": {
          "FilterRules": [
            {
              "Name": "prefix",
              "Value": "uploads/"
            },
            {
              "Name": "suffix",
              "Value": ".jpg"
            }
          ]
        }
      }
    }
  ]
}
```

### Step 9: Application Integration

**Python (boto3):**
```python
import boto3
from botocore.exceptions import ClientError

# Initialize S3 client
s3_client = boto3.client('s3', region_name='us-east-1')
s3_resource = boto3.resource('s3')

# Upload file
def upload_file(file_path, bucket, object_name=None):
    if object_name is None:
        object_name = file_path
    
    try:
        s3_client.upload_file(file_path, bucket, object_name)
        print(f"File {file_path} uploaded to {bucket}/{object_name}")
    except ClientError as e:
        print(f"Error: {e}")
        return False
    return True

# Upload with metadata and storage class
s3_client.upload_file(
    'myfile.txt',
    'my-unique-bucket-name-12345',
    'uploads/myfile.txt',
    ExtraArgs={
        'Metadata': {'author': 'John Doe', 'version': '1.0'},
        'StorageClass': 'INTELLIGENT_TIERING',
        'ServerSideEncryption': 'AES256'
    }
)

# Upload file-like object
with open('myfile.txt', 'rb') as data:
    s3_client.upload_fileobj(data, 'my-unique-bucket-name-12345', 'uploads/myfile.txt')

# Download file
s3_client.download_file(
    'my-unique-bucket-name-12345',
    'uploads/myfile.txt',
    'downloaded-file.txt'
)

# List objects
response = s3_client.list_objects_v2(
    Bucket='my-unique-bucket-name-12345',
    Prefix='uploads/'
)

for obj in response.get('Contents', []):
    print(f"{obj['Key']} - {obj['Size']} bytes - {obj['LastModified']}")

# Get object metadata
response = s3_client.head_object(
    Bucket='my-unique-bucket-name-12345',
    Key='uploads/myfile.txt'
)
print(f"Content-Type: {response['ContentType']}")
print(f"Metadata: {response['Metadata']}")

# Generate presigned URL (temporary access)
presigned_url = s3_client.generate_presigned_url(
    'get_object',
    Params={
        'Bucket': 'my-unique-bucket-name-12345',
        'Key': 'uploads/myfile.txt'
    },
    ExpiresIn=3600  # 1 hour
)
print(f"Presigned URL: {presigned_url}")

# Copy object
s3_client.copy_object(
    CopySource={'Bucket': 'my-unique-bucket-name-12345', 'Key': 'uploads/myfile.txt'},
    Bucket='my-unique-bucket-name-12345',
    Key='backup/myfile.txt'
)

# Delete object
s3_client.delete_object(
    Bucket='my-unique-bucket-name-12345',
    Key='uploads/myfile.txt'
)

# Delete multiple objects
objects_to_delete = [
    {'Key': 'file1.txt'},
    {'Key': 'file2.txt'},
    {'Key': 'file3.txt'}
]

s3_client.delete_objects(
    Bucket='my-unique-bucket-name-12345',
    Delete={'Objects': objects_to_delete}
)

# Multipart upload (for large files)
def multipart_upload(file_path, bucket, object_name):
    # Initiate multipart upload
    response = s3_client.create_multipart_upload(
        Bucket=bucket,
        Key=object_name
    )
    upload_id = response['UploadId']
    
    parts = []
    part_number = 1
    chunk_size = 5 * 1024 * 1024  # 5 MB chunks
    
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                
                # Upload part
                response = s3_client.upload_part(
                    Bucket=bucket,
                    Key=object_name,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=data
                )
                
                parts.append({
                    'PartNumber': part_number,
                    'ETag': response['ETag']
                })
                
                part_number += 1
        
        # Complete multipart upload
        s3_client.complete_multipart_upload(
            Bucket=bucket,
            Key=object_name,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )
        print(f"Multipart upload completed for {object_name}")
        
    except Exception as e:
        # Abort multipart upload on error
        s3_client.abort_multipart_upload(
            Bucket=bucket,
            Key=object_name,
            UploadId=upload_id
        )
        print(f"Multipart upload aborted: {e}")

# Using S3 resource (higher-level interface)
bucket = s3_resource.Bucket('my-unique-bucket-name-12345')

# Upload file
bucket.upload_file('myfile.txt', 'uploads/myfile.txt')

# List objects
for obj in bucket.objects.filter(Prefix='uploads/'):
    print(obj.key)

# Get object
obj = s3_resource.Object('my-unique-bucket-name-12345', 'uploads/myfile.txt')
data = obj.get()['Body'].read()
print(data.decode('utf-8'))
```

**Node.js (AWS SDK v3):**
```javascript
const {
  S3Client,
  PutObjectCommand,
  GetObjectCommand,
  ListObjectsV2Command,
  DeleteObjectCommand,
  CopyObjectCommand,
  HeadObjectCommand
} = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');
const fs = require('fs');

const s3Client = new S3Client({ region: 'us-east-1' });
const bucket = 'my-unique-bucket-name-12345';

// Upload file
async function uploadFile(filePath, key) {
  const fileContent = fs.readFileSync(filePath);
  
  const command = new PutObjectCommand({
    Bucket: bucket,
    Key: key,
    Body: fileContent,
    Metadata: {
      author: 'John Doe',
      version: '1.0'
    },
    StorageClass: 'INTELLIGENT_TIERING',
    ServerSideEncryption: 'AES256'
  });
  
  try {
    const response = await s3Client.send(command);
    console.log('Upload successful:', response);
  } catch (error) {
    console.error('Upload error:', error);
  }
}

// Download file
async function downloadFile(key, destPath) {
  const command = new GetObjectCommand({
    Bucket: bucket,
    Key: key
  });
  
  try {
    const response = await s3Client.send(command);
    const stream = response.Body;
    const writeStream = fs.createWriteStream(destPath);
    stream.pipe(writeStream);
    
    writeStream.on('finish', () => {
      console.log('Download complete');
    });
  } catch (error) {
    console.error('Download error:', error);
  }
}

// List objects
async function listObjects(prefix) {
  const command = new ListObjectsV2Command({
    Bucket: bucket,
    Prefix: prefix
  });
  
  try {
    const response = await s3Client.send(command);
    response.Contents.forEach(obj => {
      console.log(`${obj.Key} - ${obj.Size} bytes`);
    });
  } catch (error) {
    console.error('List error:', error);
  }
}

// Generate presigned URL
async function generatePresignedUrl(key, expiresIn = 3600) {
  const command = new GetObjectCommand({
    Bucket: bucket,
    Key: key
  });
  
  try {
    const url = await getSignedUrl(s3Client, command, { expiresIn });
    console.log('Presigned URL:', url);
    return url;
  } catch (error) {
    console.error('Presigned URL error:', error);
  }
}

// Copy object
async function copyObject(sourceKey, destKey) {
  const command = new CopyObjectCommand({
    CopySource: `${bucket}/${sourceKey}`,
    Bucket: bucket,
    Key: destKey
  });
  
  try {
    const response = await s3Client.send(command);
    console.log('Copy successful:', response);
  } catch (error) {
    console.error('Copy error:', error);
  }
}

// Delete object
async function deleteObject(key) {
  const command = new DeleteObjectCommand({
    Bucket: bucket,
    Key: key
  });
  
  try {
    const response = await s3Client.send(command);
    console.log('Delete successful:', response);
  } catch (error) {
    console.error('Delete error:', error);
  }
}

// Get object metadata
async function getObjectMetadata(key) {
  const command = new HeadObjectCommand({
    Bucket: bucket,
    Key: key
  });
  
  try {
    const response = await s3Client.send(command);
    console.log('Metadata:', response.Metadata);
    console.log('Content-Type:', response.ContentType);
    console.log('Size:', response.ContentLength);
  } catch (error) {
    console.error('Metadata error:', error);
  }
}

// Usage
(async () => {
  await uploadFile('myfile.txt', 'uploads/myfile.txt');
  await listObjects('uploads/');
  await downloadFile('uploads/myfile.txt', 'downloaded.txt');
  await generatePresignedUrl('uploads/myfile.txt');
  await copyObject('uploads/myfile.txt', 'backup/myfile.txt');
  await getObjectMetadata('uploads/myfile.txt');
  await deleteObject('uploads/myfile.txt');
})();
```

---

## 2. Amazon EBS (Elastic Block Store)

### What is EBS?
Block-level storage volumes for use with EC2 instances, providing persistent storage that exists independently of the instance lifecycle.

### EBS Volume Types

**General Purpose SSD (gp3, gp2):**
- **gp3** (Latest generation):
  - 3,000 IOPS baseline
  - 125 MiB/s baseline throughput
  - Can provision up to 16,000 IOPS and 1,000 MiB/s independently
  - Size: 1 GiB - 16 TiB
  - Cost-effective
- **gp2** (Previous generation):
  - IOPS scale with volume size (3 IOPS per GB)
  - Burst up to 3,000 IOPS
  - Size: 1 GiB - 16 TiB

**Provisioned IOPS SSD (io2 Block Express, io2, io1):**
- **io2 Block Express** (Latest):
  - Up to 256,000 IOPS
  - Up to 4,000 MiB/s throughput
  - Sub-millisecond latency
  - Size: 4 GiB - 64 TiB
- **io2**:
  - Up to 64,000 IOPS
  - 99.999% durability
  - Size: 4 GiB - 16 TiB
- **io1**:
  - Up to 64,000 IOPS
  - Size: 4 GiB - 16 TiB
- **Use cases**: Databases, critical applications

**Throughput Optimized HDD (st1):**
- Low-cost HDD
- Frequently accessed, throughput-intensive workloads
- 500 IOPS max
- Up to 500 MiB/s throughput
- Size: 125 GiB - 16 TiB
- **Use cases**: Big data, data warehouses, log processing
- Cannot be boot volume

**Cold HDD (sc1):**
- Lowest cost HDD
- Infrequently accessed workloads
- 250 IOPS max
- Up to 250 MiB/s throughput
- Size: 125 GiB - 16 TiB
- **Use cases**: Archival storage, infrequent access
- Cannot be boot volume

### EBS Features

**Snapshots:**
- Point-in-time backups stored in S3
- Incremental backups (only changed blocks)
- Can copy across regions
- Can create volumes from snapshots

**Encryption:**
- Encrypt volumes using KMS
- Encrypted volumes automatically encrypt:
  - Data at rest
  - Data in transit between instance and volume
  - Snapshots created from volume
  - Volumes created from snapshots

**Multi-Attach (io1/io2 only):**
- Attach same volume to multiple instances
- Up to 16 instances simultaneously
- All instances in same AZ
- Use: Clustered applications

**EBS Optimization:**
- Dedicated throughput between EC2 and EBS
- Available on most instance types
- Reduces contention

---

## Setup Guide: Amazon EBS

### Step 1: Create EBS Volume

**Console:**
```
EC2 Console → Elastic Block Store → Volumes → Create volume

Volume settings:
- Volume type: General Purpose SSD (gp3)
- Size: 100 GiB
- IOPS: 3000
- Throughput: 125 MiB/s
- Availability Zone: us-east-1a (must match EC2 instance)

Snapshot:
- Don't create volume from a snapshot (or select snapshot)

Encryption:
☑ Encrypt this volume
KMS key: (default) aws/ebs or select custom key

Tags:
Key: Name, Value: my-data-volume

Create volume
```

**CLI:**
```bash
# Create gp3 volume
aws ec2 create-volume \
    --volume-type gp3 \
    --size 100 \
    --iops 3000 \
    --throughput 125 \
    --availability-zone us-east-1a \
    --encrypted \
    --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=my-data-volume}]'

# Create io2 volume with high IOPS
aws ec2 create-volume \
    --volume-type io2 \
    --size 200 \
    --iops 10000 \
    --availability-zone us-east-1a \
    --encrypted
```

### Step 2: Attach Volume to EC2 Instance

**Console:**
```
EC2 Console → Volumes → Select volume → Actions → Attach volume

Instance: Select your EC2 instance
Device name: /dev/sdf (Linux) or xvdf

Attach volume
```

**CLI:**
```bash
aws ec2 attach-volume \
    --volume-id vol-1234567890abcdef0 \
    --instance-id i-1234567890abcdef0 \
    --device /dev/sdf
```

### Step 3: Format and Mount Volume (Linux)

**SSH into EC2 instance and execute:**

```bash
# List available disks
lsblk

# Check if volume has filesystem
sudo file -s /dev/xvdf

# If output shows "data", volume is empty and needs formatting
# Create ext4 filesystem
sudo mkfs -t ext4 /dev/xvdf

# Create mount point
sudo mkdir /data

# Mount the volume
sudo mount /dev/xvdf /data

# Verify mount
df -h

# Change ownership (optional)
sudo chown -R ec2-user:ec2-user /data

# Test write
echo "Hello from EBS" | sudo tee /data/test.txt
cat /data/test.txt
```

**Make Mount Persistent (Auto-mount on reboot):**

```bash
# Backup fstab
sudo cp /etc/fstab /etc/fstab.backup

# Get UUID of volume
sudo blkid /dev/xvdf

# Output example: /dev/xvdf: UUID="aebf131c-6957-451e-8d34-ec978d9581ae" TYPE="ext4"

# Edit fstab
sudo nano /etc/fstab

# Add this line (replace UUID with your actual UUID):
UUID=aebf131c-6957-451e-8d34-ec978d9581ae  /data  ext4  defaults,nofail  0  2

# Test fstab before reboot
sudo mount -a

# If no errors, configuration is correct
```

**For XFS filesystem (alternative to ext4):**
```bash
# Install XFS tools
sudo yum install xfsprogs -y

# Create XFS filesystem
sudo mkfs.xfs /dev/xvdf

# Mount
sudo mount /dev/xvdf /data

# Add to fstab (same process as above)
```

### Step 4: Create EBS Snapshot

**Console:**
```
EC2 Console → Volumes → Select volume → Actions → Create snapshot

Snapshot settings:
- Description: Backup of my-data-volume
- Tags:
  Key: Name, Value: my-data-volume-snapshot-2025-01-02

Create snapshot
```

**CLI:**
```bash
# Create snapshot
aws ec2 create-snapshot \
    --volume-id vol-1234567890abcdef0 \
    --description "Backup of my-data-volume" \
    --tag-specifications 'ResourceType=snapshot,Tags=[{Key=Name,Value=my-data-volume-snapshot}]'

# List snapshots
aws ec2 describe-snapshots \
    --owner-ids self \
    --query 'Snapshots[*].[SnapshotId,VolumeId,State,Progress,StartTime]' \
    --output table

# Check snapshot progress
aws ec2 describe-snapshots \
    --snapshot-ids snap-1234567890abcdef0 \
    --query 'Snapshots[0].[State,Progress]' \
    --output table
```

### Step 5: Restore Volume from Snapshot

**Console:**
```
EC2 Console → Snapshots → Select snapshot → Actions → Create volume from snapshot

Volume settings:
- Volume type: gp3
- Size: 100 GiB (or larger)
- Availability Zone: us-east-1a
- Encryption: Enable

Create volume
```

**CLI:**
```bash
aws ec2 create-volume \
    --snapshot-id snap-1234567890abcdef0 \
    --volume-type gp3 \
    --size 100 \
    --availability-zone us-east-1a \
    --encrypted
```

### Step 6: Copy Snapshot to Another Region

**Console:**
```
EC2 Console → Snapshots → Select snapshot → Actions → Copy snapshot

Destination region: US West (Oregon) us-west-2
Description: Copy of my-data-volume-snapshot
Encryption: Enable (can use different KMS key in destination region)

Copy snapshot
```

**CLI:**
```bash
aws ec2 copy-snapshot \
    --source-region us-east-1 \
    --source-snapshot-id snap-1234567890abcdef0 \
    --destination-region us-west-2 \
    --description "Copy of my-data-volume-snapshot" \
    --encrypted
```

### Step 7: Modify EBS Volume

**Increase Volume Size (No Downtime):**

```bash
# Modify volume via CLI
aws ec2 modify-volume \
    --volume-id vol-1234567890abcdef0 \
    --size 200 \
    --volume-type gp3 \
    --iops 5000 \
    --throughput 250

# Check modification status
aws ec2 describe-volumes-modifications \
    --volume-ids vol-1234567890abcdef0
```

**Extend Filesystem After Resize:**

```bash
# Check current filesystem size
df -h /data

# For ext4 filesystem
sudo resize2fs /dev/xvdf

# For XFS filesystem
sudo xfs_growfs /data

# Verify new size
df -h /data
```

### Step 8: Detach and Delete Volume

**Detach Volume:**

```bash
# Unmount first
sudo umount /data

# Remove from fstab
sudo nano /etc/fstab
# Comment out or remove the volume's entry

# Detach via AWS
aws ec2 detach-volume --volume-id vol-1234567890abcdef0
```

**Delete Volume:**

```bash
# Console: EC2 → Volumes → Select volume → Actions → Delete volume

# CLI
aws ec2 delete-volume --volume-id vol-1234567890abcdef0
```

### Step 9: EBS Snapshot Automation (Data Lifecycle Manager)

**Console:**
```
EC2 Console → Elastic Block Store → Lifecycle Manager → Create lifecycle policy

Policy type: EBS snapshot policy

Target resources:
- Target resource types: Volume
- Target resource tags:
  Key: Backup, Value: true

Schedule:
- Policy schedule name: daily-backup
- Frequency: Daily
- Starting at: 03:00 UTC
- Retention type: Count
- Retain: 7 snapshots

Tagging:
☑ Copy tags from source
Additional tags:
  Key: CreatedBy, Value: DLM

IAM role: Default role (or create custom)

Create policy
```

**CLI:**
```bash
aws dlm create-lifecycle-policy \
    --execution-role-arn arn:aws:iam::123456789012:role/AWSDataLifecycleManagerDefaultRole \
    --description "Daily EBS snapshots" \
    --state ENABLED \
    --policy-details file://dlm-policy.json
```

**dlm-policy.json:**
```json
{
  "ResourceTypes": ["VOLUME"],
  "TargetTags": [
    {
      "Key": "Backup",
      "Value": "true"
    }
  ],
  "Schedules": [
    {
      "Name": "daily-backup",
      "CopyTags": true,
      "TagsToAdd": [
        {
          "Key": "CreatedBy",
          "Value": "DLM"
        }
      ],
      "CreateRule": {
        "Interval": 24,
        "IntervalUnit": "HOURS",
        "Times": ["03:00"]
      },
      "RetainRule": {
        "Count": 7
      }
    }
  ]
}
```

---

## 3. Amazon EFS (Elastic File System)

### What is EFS?
Fully managed, scalable, elastic NFS file system for use with AWS Cloud services and on-premises resources. Multiple EC2 instances can access an EFS file system simultaneously.

### Key Features

**Elastic and Scalable:**
- Automatically grows and shrinks
- Petabyte-scale storage
- No capacity planning needed

**Performance Modes:**
- **General Purpose**: Low latency (default)
- **Max I/O**: Higher aggregate throughput and IOPS

**Throughput Modes:**
- **Bursting**: Throughput scales with file system size
- **Provisioned**: Set throughput independent of size
- **Elastic**: Automatically scales throughput up and down

**Storage Classes:**
- **Standard**: Frequently accessed files
- **Infrequent Access (IA)**: Lower cost for infrequently accessed files
- **Archive**: Lowest cost for rarely accessed files (up to 90% savings)

**Access:**
- Multi-AZ access (Regional)
- One Zone (lower cost, single AZ)
- Cross-region access via VPC peering
- On-premises access via Direct Connect or VPN

---

## Setup Guide: Amazon EFS

### Step 1: Create EFS File System

**Console:**
```
EFS Console → File systems → Create file system

Quick create (Recommended) or Customize:

File system settings:
- Name: my-efs-filesystem
- Availability and durability: Regional (or One Zone)
- Automatic backups: Enable

Performance settings:
- Performance mode: General Purpose
- Throughput mode: Elastic (or Bursting/Provisioned)

Network settings:
- Virtual Private Cloud (VPC): Select your VPC
- Mount targets: Create mount targets in each AZ
  - AZ 1: us-east-1a, Subnet, Security group
  - AZ 2: us-east-1b, Subnet, Security group
  - AZ 3: us-east-1c, Subnet, Security group

File system policy: [Optional]

Encryption:
☑ Enable encryption of data at rest
KMS key: aws/elasticfilesystem or custom key

Lifecycle management:
- Transition into IA: 30 days since last access
- Transition into Archive: 90 days since last access
- Transition out of IA: On first access

Tags:
Key: Environment, Value: Production

Create
```

**CLI:**
```bash
# Create file system
aws efs create-file-system \
    --creation-token my-efs-filesystem \
    --performance-mode generalPurpose \
    --throughput-mode elastic \
    --encrypted \
    --tags Key=Name,Value=my-efs-filesystem

# Get file system ID from output
# Example: fs-1234567890abcdef0

# Create mount targets (one per AZ)
aws efs create-mount-target \
    --file-system-id fs-1234567890abcdef0 \
    --subnet-id subnet-12345678 \
    --security-groups sg-1234567890abcdef0

aws efs create-mount-target \
    --file-system-id fs-1234567890abcdef0 \
    --subnet-id subnet-87654321 \
    --security-groups sg-1234567890abcdef0
```

### Step 2: Configure Security Group

**Security Group Rules for EFS:**
```
Inbound Rules:
Type: NFS
Protocol: TCP
Port: 2049
Source: EC2 instance security group or VPC CIDR
Description: Allow NFS access from EC2 instances
```

**CLI:**
```bash
aws ec2 authorize-security-group-ingress \
    --group-id sg-efs-mount-target \
    --protocol tcp \
    --port 2049 \
    --source-group sg-ec2-instances
```

### Step 3: Mount EFS on EC2 Instance

**Install EFS Mount Helper (Amazon Linux 2):**
```bash
sudo yum install -y amazon-efs-utils
```

**Ubuntu:**
```bash
sudo apt-get update
sudo apt-get -y install git binutils
git clone https://github.com/aws/efs-utils
cd efs-utils
./build-deb.sh
sudo apt-get -y install ./build/amazon-efs-utils*deb
```

**Mount using EFS mount helper:**
```bash
# Create mount point
sudo mkdir /mnt/efs

# Mount EFS (replace fs-1234567890abcdef0 with your file system ID)
sudo mount -t efs -o tls fs-1234567890abcdef0:/ /mnt/efs

# Verify mount
df -h | grep efs

# Test write
sudo touch /mnt/efs/test-file.txt
echo "Hello from EFS" | sudo tee /mnt/efs/test-file.txt
```

**Mount with encryption in transit:**
```bash
sudo mount -t efs -o tls fs-1234567890abcdef0:/ /mnt/efs
```

**Mount using NFS client (without EFS utils):**
```bash
# Install NFS client
sudo yum install -y nfs-utils

# Mount (replace DNS name with your mount target DNS)
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport \
    fs-1234567890abcdef0.efs.us-east-1.amazonaws.com:/ /mnt/efs
```

**Make Mount Persistent:**
```bash
# Edit fstab
sudo nano /etc/fstab

# Add this line (using EFS mount helper with encryption):
fs-1234567890abcdef0:/ /mnt/efs efs _netdev,tls,iam 0 0

# Or using NFS:
fs-1234567890abcdef0.efs.us-east-1.amazonaws.com:/ /mnt/efs nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,_netdev 0 0

# Test mount
sudo mount -a
```

### Step 4: Configure Lifecycle Management

**Console:**
```
EFS Console → File systems → Select your file system → 
  File system settings → Lifecycle management → Edit

Lifecycle policies:
- Transition into IA: 30 days since last access
- Transition into Archive: 90 days since last access
- Transition out of IA: On first access

Save
```

**CLI:**
```bash
aws efs put-lifecycle-configuration \
    --file-system-id fs-1234567890abcdef0 \
    --lifecycle-policies \
        TransitionToIA=AFTER_30_DAYS \
        TransitionToArchive=AFTER_90_DAYS \
        TransitionToPrimaryStorageClass=AFTER_1_ACCESS
```

### Step 5: Setup EFS Access Points

**Access points provide application-specific entry points into an EFS file system:**

**Console:**
```
EFS Console → File systems → Select file system → 
  Access points → Create access point

Access point details:
- Name: my-app-access-point
- Root directory path: /app-data
  ☑ Create directory if it doesn't exist
  Owner user ID: 1000
  Owner group ID: 1000
  Permissions: 0755

POSIX user:
- User ID: 1000
- Group ID: 1000
- Secondary group IDs: [Optional]

Create access point
```

**CLI:**
```bash
aws efs create-access-point \
    --file-system-id fs-1234567890abcdef0 \
    --posix-user Uid=1000,Gid=1000 \
    --root-directory "Path=/app-data,CreationInfo={OwnerUid=1000,OwnerGid=1000,Permissions=0755}" \
    --tags Key=Name,Value=my-app-access-point
```

**Mount using Access Point:**
```bash
sudo mount -t efs -o tls,accesspoint=fsap-1234567890abcdef0 fs-1234567890abcdef0:/ /mnt/efs-app
```

### Step 6: Monitor EFS Performance

**CloudWatch Metrics:**
```
- ClientConnections
- DataReadIOBytes
- DataWriteIOBytes
- MetadataIOBytes
- PercentIOLimit (for bursting mode)
- PermittedThroughput
- TotalIOBytes
- BurstCreditBalance
```

**CLI - Get Metrics:**
```bash
aws cloudwatch get-metric-statistics \
    --namespace AWS/EFS \
    --metric-name TotalIOBytes \
    --dimensions Name=FileSystemId,Value=fs-1234567890abcdef0 \
    --start-time 2025-01-02T00:00:00Z \
    --end-time 2025-01-02T23:59:59Z \
    --period 3600 \
    --statistics Sum
```

---

## 4. Amazon FSx

### What is FSx?
Fully managed third-party file systems optimized for specific workloads.

### FSx Options

**FSx for Windows File Server:**
- Native Windows file system
- SMB protocol support
- Active Directory integration
- DFS namespaces
- Use: Windows applications, .NET apps

**FSx for Lustre:**
- High-performance computing file system
- Sub-millisecond latencies
- Integration with S3
- Use: ML, HPC, video processing

**FSx for NetApp ONTAP:**
- NetApp's ONTAP file system
- Multi-protocol (NFS, SMB, iSCSI)
- Advanced data management
- Use: Enterprise applications

**FSx for OpenZFS:**
- OpenZFS file system
- NFS protocol
- Point-in-time snapshots
- Use: Linux workloads, database workloads

---

## Setup Guide: FSx for Windows File Server

### Step 1: Create FSx File System

**Console:**
```
FSx Console → File systems → Create file system

File system type: Amazon FSx for Windows File Server

File system details:
- Deployment type: Multi-AZ (or Single-AZ)
- Storage type: SSD (or HDD for throughput-optimized)
- Storage capacity: 300 GB (minimum 32 GB)
- Throughput capacity: 32 MB/s

Network & security:
- VPC: Select your VPC
- VPC security groups: Select or create
- Subnet: Select subnets

Windows authentication:
- AWS Managed Microsoft Active Directory (or Self-managed AD)
- Directory: Select directory

Encryption:
☑ Encryption of data at rest
KMS key: aws/fsx or custom key

Backup and maintenance:
- Daily automatic backup: Enable
- Backup retention: 7 days
- Preferred backup window: No preference
- Preferred maintenance window: No preference

Tags:
Key: Name, Value: my-fsx-windows-fs

Create file system
```

**CLI:**
```bash
aws fsx create-file-system \
    --file-system-type WINDOWS \
    --storage-capacity 300 \
    --subnet-ids subnet-12345678 subnet-87654321 \
    --security-group-ids sg-1234567890abcdef0 \
    --windows-configuration '{
        "ThroughputCapacity": 32,
        "DeploymentType": "MULTI_AZ_1",
        "PreferredSubnetId": "subnet-12345678",
        "ActiveDirectoryId": "d-1234567890"
    }' \
    --tags Key=Name,Value=my-fsx-windows-fs
```

### Step 2: Mount FSx on Windows Instance

**On Windows EC2 Instance:**

```powershell
# Get DNS name from FSx console
# Example: amznfsxabcd1234.example.com

# Map network drive
net use Z: \\amznfsxabcd1234.example.com\share /persistent:yes

# Or use File Explorer:
# This PC → Map network drive → 
#   Drive: Z:
#   Folder: \\amznfsxabcd1234.example.com\share
#   ☑ Reconnect at sign-in
```

**PowerShell Script:**
```powershell
$dnsName = "amznfsxabcd1234.example.com"
$driveLetter = "Z:"
$sharePath = "\\$dnsName\share"

New-PSDrive -Name $driveLetter.TrimEnd(':') `
            -PSProvider FileSystem `
            -Root $sharePath `
            -Persist

# Verify
Get-PSDrive
```

### Step 3: Create and Manage Shares

**PowerShell (on FSx file system):**
```powershell
# Create new share
New-FSxSmbShare -Name "data" `
                -Path "D:\data" `
                -Description "Data share" `
                -ContinuouslyAvailable $true

# Grant permissions
Grant-FSxSmbShareAccess -Name "data" `
                        -AccountName "DOMAIN\User" `
                        -AccessRight Full

# View shares
Get-FSxSmbShare
```

---

## 5. AWS Storage Gateway

### What is Storage Gateway?
Hybrid cloud storage service that connects on-premises environments to AWS cloud storage, providing seamless and secure integration.

### Gateway Types

**File Gateway (NFS/SMB):**
- Stores files as objects in S3
- Local cache for frequently accessed data
- Use: File shares, NAS replacement

**Volume Gateway:**
- Block storage volumes backed by S3
- **Stored Mode**: Primary data on-premises, async backup to AWS
- **Cached Mode**: Primary data in AWS, frequently accessed data cached locally
- Use: Backup, disaster recovery

**Tape Gateway:**
- Virtual tape library backed by S3/Glacier
- Compatible with existing backup software
- Use: Long-term archive, tape replacement

---

## Setup Guide: AWS Storage Gateway (File Gateway)

### Step 1: Deploy Gateway

**Choose Deployment Option:**
- VMware ESXi
- Microsoft Hyper-V
- Linux KVM
- Amazon EC2
- Hardware appliance

**Using EC2:**

```bash
# Launch Storage Gateway AMI from AWS Marketplace
# t2.xlarge or larger recommended
# Minimum 80 GB root volume + cache disk

# Console:
EC2 → Launch Instance → AWS Marketplace → 
  Search "AWS Storage Gateway" → Select → Launch
```

### Step 2: Activate Gateway

**Console:**
```
Storage Gateway Console → Gateways → Create gateway

Gateway options:
- Gateway name: my-file-gateway
- Gateway time zone: (GMT-5:00) Eastern Time
- Gateway type: Amazon S3 File Gateway

Connection options:
- Endpoint type: Publicly accessible
- IP address: [Gateway EC2 public IP]

Activate gateway
```

**Access Gateway Console:**
```
http://[gateway-ip-address]

# Configure local disks:
# - Root disk: Operating system
# - Cache disk: 150 GB minimum (local cache)
# - Upload buffer: Pending uploads to S3

# Assign disks and configure
```

### Step 3: Create File Share

**Console:**
```
Storage Gateway Console → File shares → Create file share

Gateway: Select my-file-gateway

File share settings:
- Amazon S3 bucket name: my-gateway-bucket
- AWS Region: us-east-1
- Access via: NFS (or SMB)
- Storage class: S3 Standard (or Intelligent-Tiering)

Access objects using:
☑ Access based on POSIX file permissions

Automated cache refresh from S3:
☑ Refresh cache (optional)
- Refresh interval: 5 minutes

Tags:
Key: Name, Value: my-nfs-share

Create file share
```

### Step 4: Mount File Share (Linux)

**On-premises Linux Server:**

```bash
# Install NFS client
sudo yum install -y nfs-utils

# Create mount point
sudo mkdir -p /mnt/gateway-share

# Mount file share (replace with your gateway IP and export path)
sudo mount -t nfs -o nolock,hard,nfsvers=3 \
    192.168.1.100:/my-gateway-bucket /mnt/gateway-share

# Verify
df -h | grep gateway

# Make persistent
echo "192.168.1.100:/my-gateway-bucket /mnt/gateway-share nfs nolock,hard,nfsvers=3,_netdev 0 0" | \
    sudo tee -a /etc/fstab

# Test write
echo "Hello from Storage Gateway" | sudo tee /mnt/gateway-share/test.txt

# Verify in S3 (will appear after upload buffer flushes)
aws s3 ls s3://my-gateway-bucket/
```

---

## 6. AWS DataSync

### What is DataSync?
Automated data transfer service that moves data between on-premises storage and AWS, or between AWS storage services.

### Key Features
- Up to 10 times faster than open-source tools
- Handles data verification
- Automatic encryption
- Bandwidth throttling
- Scheduling

### Use Cases
- Data migration to AWS
- Data replication for DR
- Archival to S3 Glacier
- Data distribution

---

## Setup Guide: AWS DataSync

### Step 1: Deploy DataSync Agent (On-Premises)

**Download Agent:**
```
DataSync Console → Agents → Create agent → 
  Download VM image for:
  - VMware ESXi
  - Microsoft Hyper-V
  - Linux KVM

Deploy OVA/VHD on your hypervisor
Configure with:
  - 4 vCPUs (minimum)
  - 32 GB RAM (minimum)
  - 80 GB disk
```

### Step 2: Activate Agent

**Console:**
```
DataSync Console → Agents → Create agent

Activation key options:
- Service endpoint: Public service endpoints
- Agent address: [Agent IP address]

Get key (automatically activates agent)

Agent configuration:
- Agent name: my-datasync-agent
- VPC endpoints: [Optional - for private connectivity]

Create agent
```

### Step 3: Create Source Location

**For NFS Source:**

```
DataSync Console → Locations → Create location

Location type: Network File System (NFS)

Agents: Select my-datasync-agent

NFS server:
- Server hostname or IP: 192.168.1.50
- Export path: /data

Mount options:
- NFS version: Automatic

Create location
```

### Step 4: Create Destination Location

**For S3 Destination:**

```
DataSync Console → Locations → Create location

Location type: Amazon S3

S3 bucket: my-destination-bucket
S3 storage class: Intelligent-Tiering

IAM role: Create new role (DataSync will create automatically)

Create location
```

### Step 5: Create Task

**Console:**
```
DataSync Console → Tasks → Create task

Source location: Select NFS location
Destination location: Select S3 location

Task name: sync-onprem-to-s3

Task settings:
Data transfer configuration:
- Bandwidth limit: No limit (or specify MB/s)
- Object metadata: Preserve
- Ownership and permissions: Preserve POSIX permissions

Data verification:
☑ Verify data during transfer

Filtering:
- Include patterns: [Optional]
- Exclude patterns: [Optional, e.g., *.tmp, .git/*]

Task scheduling:
- Schedule: Manual (or Scheduled)
If scheduled:
  - Frequency: Every 1 day
  - Start time: 02:00 UTC

Task logging:
- Log level: Log all transferred objects and files
- CloudWatch Log group: Create new

Create task
```

### Step 6: Run Task

**Console:**
```
DataSync Console → Tasks → Select task → Start

Verify data transfer
```

**CLI:**
```bash
# Start task
aws datasync start-task-execution \
    --task-arn arn:aws:datasync:us-east-1:123456789012:task/task-1234567890abcdef0

# Monitor progress
aws datasync describe-task-execution \
    --task-execution-arn arn:aws:datasync:us-east-1:123456789012:task/task-1234567890abcdef0/execution/exec-1234567890abcdef0
```

---

## 7. AWS Backup

### What is AWS Backup?
Fully managed backup service that centralizes and automates data protection across AWS services.

### Supported Services
- EC2 instances
- EBS volumes
- RDS databases
- DynamoDB tables
- EFS file systems
- FSx file systems
- Storage Gateway volumes
- DocumentDB
- Neptune

---

## Setup Guide: AWS Backup

### Step 1: Create Backup Vault

**Console:**
```
AWS Backup Console → Backup vaults → Create backup vault

Backup vault name: my-backup-vault

Encryption key: 
- Use an AWS Backup managed key (or custom KMS key)

Tags:
Key: Environment, Value: Production

Create backup vault
```

### Step 2: Create Backup Plan

**Console:**
```
AWS Backup Console → Backup plans → Create backup plan

Choose option:
• Start with a template (recommended for beginners)
• Build a new plan
• Define a plan using JSON

Using template:

Backup plan name: daily-backup-plan

Backup rule configuration:
Rule name: DailyBackup

Schedule:
- Frequency: Daily
- Backup window: 
  ☐ Use backup window defaults (or customize)
  Start time: 05:00 UTC
  Duration: 8 hours (start within)
  
Transition to cold storage: After 30 days
Retention period: 90 days

Backup vault: my-backup-vault

Advanced backup settings:
☑ Enable Continuous Backup for point-in-time recovery

Create backup plan
```

**JSON Example:**
```json
{
  "BackupPlanName": "daily-backup-plan",
  "Rules": [
    {
      "RuleName": "DailyBackup",
      "ScheduleExpression": "cron(0 5 * * ? *)",
      "StartWindowMinutes": 480,
      "TargetBackupVaultName": "my-backup-vault",
      "Lifecycle": {
        "MoveToColdStorageAfterDays": 30,
        "DeleteAfterDays": 90
      },
      "RecoveryPointTags": {
        "BackupType": "Automated"
      },
      "EnableContinuousBackup": true
    }
  ]
}
```

### Step 3: Assign Resources

**Console:**
```
Backup plan → Resource assignments → Assign resources

Resource assignment name: ec2-and-ebs-backup

IAM role: Default role (or create custom)

Resource selection:
• Include all resource types
• Include specific resource types:
  ☑ EC2
  ☑ EBS

Assign by:
• Resource ID
• Tags
  Key: Backup
  Value: true
  Condition: STRINGEQUALS

Assign resources
```

**All resources matching the tags will be automatically backed up**

### Step 4: Restore from Backup

**Console:**
```
AWS Backup Console → Protected resources → 
  Select resource → View details → 
  Recovery points → Select recovery point → Restore

Restore configuration (example for EC2):
Instance type: t3.micro
Virtual Private Cloud: Select VPC
Subnet: Select subnet
Security groups: Select security groups
Instance IAM role: Select role
Shutdown behavior: Stop

Restore backup
```

**CLI Example (EBS):**
```bash
# List recovery points
aws backup list-recovery-points-by-backup-vault \
    --backup-vault-name my-backup-vault

# Start restore job
aws backup start-restore-job \
    --recovery-point-arn arn:aws:backup:us-east-1:123456789012:recovery-point:1234567890abcdef0 \
    --iam-role-arn arn:aws:iam::123456789012:role/AWSBackupDefaultServiceRole \
    --metadata '{
        "AvailabilityZone": "us-east-1a",
        "VolumeType": "gp3",
        "Encrypted": "true"
    }'
```

---

## Storage Service Selection Guide

### Choose S3 When:
- ✅ Object storage needs
- ✅ Static website hosting
- ✅ Data lakes
- ✅ Backup and archival
- ✅ Application data storage
- ✅ Big data analytics

### Choose EBS When:
- ✅ Block storage for EC2
- ✅ Database storage
- ✅ Boot volumes
- ✅ High IOPS requirements
- ✅ Single instance access

### Choose EFS When:
- ✅ Shared file storage
- ✅ Multiple EC2 instances need access
- ✅ Linux workloads (NFS)
- ✅ Content management systems
- ✅ Web serving
- ✅ Container storage

### Choose FSx When:
- ✅ Windows file shares (FSx for Windows)
- ✅ High
