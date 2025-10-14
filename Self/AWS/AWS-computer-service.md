<img width="1400" height="804" alt="image" src="https://github.com/user-attachments/assets/7a1f1bf8-c476-48e5-9e61-b4a9e83de14a" />

# AWS Compute Services - Beyond EC2 and Lambda

## Overview
AWS offers a comprehensive suite of compute services beyond traditional EC2 instances and Lambda functions, categorized into five main groups: Instance, Containers, Serverless, Edge and Hybrid, and Cost and Capacity Management.

---

## 1. Instance-Based Compute

### Amazon EC2 (Elastic Compute Cloud)
- **Description**: Virtual servers in the cloud
- **Use Cases**: 
  - General-purpose computing
  - Full control over OS and configuration
  - Long-running applications
  - Custom software stacks
- **Features**:
  - Multiple instance types and sizes
  - Pay-as-you-go or reserved pricing
  - Complete root access

### Amazon EC2 Spot
- **Description**: Unused EC2 capacity at discounted rates (up to 90% off)
- **Use Cases**:
  - Fault-tolerant workloads
  - Batch processing
  - Big data analysis
  - CI/CD workloads
  - Stateless web servers
- **Key Considerations**:
  - Can be interrupted with 2-minute warning
  - Best for flexible, interruptible workloads
  - Significant cost savings

### Amazon EC2 Autoscaling
- **Description**: Automatically adjust EC2 capacity based on demand
- **Features**:
  - Dynamic scaling policies
  - Scheduled scaling
  - Predictive scaling using ML
  - Health checks and replacement
  - Integration with ELB
- **Benefits**:
  - Cost optimization
  - Maintain application availability
  - Handle traffic spikes automatically

### Amazon Lightsail
- **Description**: Simplified virtual private servers (VPS)
- **Use Cases**:
  - Simple web applications
  - Websites and blogs
  - Development/test environments
  - Small business applications
- **Features**:
  - Predictable, low monthly pricing
  - Pre-configured application stacks
  - Easy-to-use management console
  - Integrated networking and storage
- **Target Audience**: Developers who need simple cloud infrastructure

### AWS Batch
- **Description**: Fully managed batch processing at any scale
- **Use Cases**:
  - Data processing pipelines
  - Scientific simulations
  - Financial modeling
  - Image/video rendering
  - Genomics analysis
- **Features**:
  - Automatically provisions optimal compute resources
  - Job scheduling and queuing
  - Integration with EC2, Spot, and Fargate
  - No infrastructure management

---

## 2. Container-Based Compute

### Amazon ECS (Elastic Container Service)
- **Description**: Fully managed container orchestration service
- **Use Cases**:
  - Microservices architectures
  - Batch processing
  - Machine learning applications
- **Features**:
  - Deep AWS integration
  - Support for Docker containers
  - Launch types: EC2 or Fargate
  - Task definitions and services
  - Integration with ALB/NLB

### Amazon ECR (Elastic Container Registry)
- **Description**: Fully managed Docker container registry
- **Features**:
  - Store, manage, and deploy container images
  - Secure, scalable, and reliable
  - Image scanning for vulnerabilities
  - Integration with ECS and EKS
  - Cross-region and cross-account replication
- **Benefits**:
  - No infrastructure to manage
  - High availability
  - Encryption at rest and in transit

### Amazon EKS (Elastic Kubernetes Service)
- **Description**: Managed Kubernetes service
- **Use Cases**:
  - Complex containerized applications
  - Organizations using Kubernetes
  - Multi-cloud strategies
  - Hybrid deployments
- **Features**:
  - Certified Kubernetes conformant
  - Automatic updates and patching
  - Integration with AWS services
  - Support for spot instances
  - Self-managed or managed node groups

### AWS Fargate
- **Description**: Serverless compute engine for containers
- **Use Cases**:
  - Microservices without infrastructure management
  - Batch jobs
  - Applications requiring isolation
- **Features**:
  - No EC2 instance management
  - Pay only for resources used
  - Works with both ECS and EKS
  - Automatic scaling
  - Built-in security isolation
- **Benefits**:
  - Focus on applications, not infrastructure
  - Right-sizing per task
  - Improved security posture

---

## 3. Serverless Compute

### AWS Lambda
- **Description**: Run code without provisioning servers
- **Use Cases**:
  - Event-driven processing
  - Real-time file processing
  - API backends (with API Gateway)
  - Stream processing
  - Scheduled tasks (cron jobs)
  - Automation and orchestration
- **Features**:
  - Automatic scaling
  - Pay per request and compute time
  - Support for multiple languages
  - 15-minute max execution time
  - Event source integrations
  - Stateless execution
- **Pricing Model**:
  - Free tier: 1M requests/month
  - Pay for invocations and duration
  - No charge when code isn't running

---

## 4. Edge and Hybrid Compute

### AWS Outposts
- **Description**: AWS infrastructure on-premises
- **Use Cases**:
  - Low-latency applications
  - Data residency requirements
  - Local data processing
  - Hybrid cloud architectures
- **Features**:
  - Same AWS APIs and tools
  - AWS-managed infrastructure
  - Available in various configurations
  - Consistent hybrid experience
- **Services Available**: EC2, EBS, S3, ECS, RDS, EMR

### AWS Snow Family
- **Description**: Physical devices for data transfer and edge computing
- **Types**:
  - **Snowcone**: Smallest (8TB), edge computing
  - **Snowball**: Medium (50-80TB), data transfer
  - **Snowmobile**: Largest (100PB), exabyte-scale
- **Use Cases**:
  - Large-scale data migrations
  - Disaster recovery
  - Edge computing in remote locations
  - Content distribution
- **Features**:
  - Ruggedized devices
  - Encryption and security
  - Computing capabilities on some devices

### AWS Wavelength
- **Description**: AWS compute at 5G network edge
- **Use Cases**:
  - Ultra-low latency applications (single-digit milliseconds)
  - AR/VR applications
  - Real-time gaming
  - Live video streaming
  - ML inference at edge
- **Features**:
  - Embedded in telecom provider networks
  - Direct access from 5G devices
  - Standard AWS services (EC2, ECS, EKS)
  - No additional charges for Wavelength usage

### VMware Cloud on AWS
- **Description**: Run VMware workloads on AWS infrastructure
- **Use Cases**:
  - Migrate VMware VMs to AWS
  - Hybrid cloud deployments
  - Disaster recovery for VMware environments
  - Data center extension
- **Features**:
  - Native VMware software stack
  - Same tools and processes
  - Seamless integration with AWS services
  - On-demand, elastic infrastructure

### AWS Local Zones
- **Description**: AWS infrastructure closer to large population centers
- **Use Cases**:
  - Single-digit millisecond latency applications
  - Media & entertainment rendering
  - Live gaming
  - Real-time analytics
  - Machine learning inference
- **Features**:
  - Extension of AWS region
  - Same AWS APIs
  - Local VPC subnets
  - Support for EC2, EBS, VPC, ELB

---

## 5. Cost and Capacity Management

### AWS Savings Plans
- **Description**: Flexible pricing model for compute usage
- **Types**:
  - **Compute Savings Plans**: Most flexible (EC2, Lambda, Fargate)
  - **EC2 Instance Savings Plans**: Specific instance families
- **Features**:
  - Up to 72% savings vs. on-demand
  - 1 or 3-year commitment
  - Automatic application to usage
  - Flexible across instance types, regions, OS
- **Benefits**:
  - Lower costs than reserved instances
  - More flexibility than reserved instances

### AWS Compute Optimizer
- **Description**: ML-powered recommendations for optimal AWS resources
- **Features**:
  - Analyzes historical utilization
  - Recommends optimal instance types
  - Identifies over/under-provisioned resources
  - Cost and performance projections
- **Supported Services**:
  - EC2 instances
  - Auto Scaling groups
  - EBS volumes
  - Lambda functions
- **Benefits**:
  - Reduce costs by up to 25%
  - Improve performance
  - Data-driven decision making

### AWS Elastic Beanstalk
- **Description**: Platform-as-a-Service (PaaS) for deploying applications
- **Use Cases**:
  - Web applications
  - API backends
  - Microservices
  - Quick deployments
- **Features**:
  - Automatic capacity provisioning
  - Load balancing and auto-scaling
  - Health monitoring
  - Support for multiple languages and platforms
  - Managed platform updates
- **Benefits**:
  - Focus on code, not infrastructure
  - Developer-friendly
  - Full control when needed (can access underlying resources)
  - No additional charge (pay for underlying resources)

### EC2 Image Builder
- **Description**: Automate creation, maintenance, and deployment of OS images
- **Use Cases**:
  - Standardized AMI creation
  - Security patching automation
  - Compliance requirements
  - Golden image pipelines
- **Features**:
  - Automated build pipeline
  - Built-in security testing
  - Version management
  - Cross-region distribution
  - Integration with Systems Manager
- **Benefits**:
  - Reduce manual effort
  - Consistent, secure images
  - Automated updates and patching

### Elastic Load Balancing (ELB)
- **Description**: Automatically distribute traffic across multiple targets
- **Types**:
  - **Application Load Balancer (ALB)**: Layer 7 (HTTP/HTTPS)
  - **Network Load Balancer (NLB)**: Layer 4 (TCP/UDP), ultra-low latency
  - **Gateway Load Balancer (GWLB)**: Layer 3, for third-party appliances
  - **Classic Load Balancer (CLB)**: Legacy, both Layer 4 and 7
- **Features**:
  - High availability across AZs
  - Health checks
  - SSL/TLS termination
  - Integration with Auto Scaling
  - WebSocket support
- **Use Cases**:
  - Distribute application traffic
  - Achieve fault tolerance
  - Seamless scaling

---

## Service Selection Guide

### Choose Based on Your Needs:

**Full Control & Customization**
- Amazon EC2 (traditional instances)
- EC2 Spot (cost-optimized)

**Containers**
- ECS (AWS-native)
- EKS (Kubernetes)
- Fargate (serverless containers)

**Serverless**
- Lambda (event-driven functions)

**Simple/Managed Solutions**
- Lightsail (simple VPS)
- Elastic Beanstalk (PaaS)

**Batch Processing**
- AWS Batch (large-scale batch jobs)

**Edge Computing**
- Wavelength (5G/ultra-low latency)
- Local Zones (single-digit ms latency)
- Lambda@Edge (CDN compute)

**Hybrid/On-Premises**
- Outposts (on-premises AWS)
- VMware Cloud (VMware workloads)
- Snow Family (data transfer + edge)

**Cost Optimization**
- Savings Plans (commitment-based savings)
- Compute Optimizer (recommendations)
- Spot Instances (discount capacity)

---

## Best Practices

### Cost Optimization
- Use Compute Optimizer for right-sizing
- Consider Spot instances for fault-tolerant workloads
- Purchase Savings Plans for predictable workloads
- Use Auto Scaling to match demand

### Performance
- Choose the right instance type for workload
- Use placement groups for HPC workloads
- Leverage Local Zones for latency-sensitive applications
- Use load balancers for distribution

### Scalability
- Implement Auto Scaling
- Use serverless where appropriate
- Design for horizontal scaling
- Use managed services to reduce operational burden

### Security
- Use IAM roles instead of credentials
- Enable encryption at rest and in transit
- Scan container images (ECR)
- Implement least privilege access
- Use VPC for network isolation


# Amazon EC2 and AWS Lambda - Deep Dive

---

## Amazon EC2 (Elastic Compute Cloud)

### What is EC2?
Amazon EC2 is a web service that provides **resizable compute capacity in the cloud**. It's essentially virtual servers (called instances) that you can launch, configure, and manage as needed.

Think of it as: **Renting a computer in the cloud that you have complete control over**

---

## EC2 Core Concepts

### 1. EC2 Instances
Virtual servers running in AWS data centers

**Instance Components:**
- **vCPUs**: Virtual processors
- **Memory (RAM)**: Instance memory
- **Storage**: EBS volumes or instance store
- **Network**: Network interface cards (ENIs)
- **Operating System**: Your choice (Linux, Windows, etc.)

### 2. Amazon Machine Image (AMI)
Template that contains the software configuration (OS, application server, applications)

**Types of AMIs:**
- **AWS-provided**: Amazon Linux, Ubuntu, Windows Server, etc.
- **Marketplace AMIs**: Pre-configured by third parties
- **Community AMIs**: Shared by other AWS users
- **Custom AMIs**: Your own created images

**AMI includes:**
- Root volume template
- Launch permissions
- Block device mapping

### 3. Instance Types
Different combinations of CPU, memory, storage, and networking capacity

**Instance Type Naming Convention:**
```
Example: m5.2xlarge
- m = Instance family
- 5 = Generation
- 2xlarge = Size
```

**Instance Families:**

**General Purpose (T, M, A)**
- **T3/T4g**: Burstable performance (web servers, dev environments)
- **M5/M6**: Balanced compute, memory, networking
- **Use cases**: Web applications, small databases, dev/test

**Compute Optimized (C)**
- **C5/C6**: High-performance processors
- **Use cases**: Batch processing, gaming servers, HPC, scientific modeling

**Memory Optimized (R, X, Z)**
- **R5/R6**: Large memory for in-memory databases
- **X1e/X2**: Extreme memory (up to 4TB RAM)
- **Use cases**: SAP HANA, in-memory databases, big data processing

**Storage Optimized (I, D, H)**
- **I3/I4i**: High IOPS, NVMe SSD
- **D2/D3**: Dense HDD storage
- **Use cases**: NoSQL databases, data warehousing, Hadoop

**Accelerated Computing (P, G, F, Inf)**
- **P4/P3**: GPU for machine learning training
- **G4/G5**: GPU for graphics and ML inference
- **F1**: FPGA instances
- **Inf1**: AWS Inferentia chips for ML inference
- **Use cases**: ML, video encoding, graphics workstations

### 4. Instance Purchasing Options

**On-Demand Instances**
- Pay by the second (Linux) or hour (Windows)
- No upfront commitment
- **Use when**: Unpredictable workloads, testing, short-term applications
- **Cost**: Highest per-hour rate

**Reserved Instances (RI)**
- 1 or 3-year commitment
- Up to 75% discount vs. on-demand
- **Types**:
  - Standard RI: Highest discount, fixed instance type
  - Convertible RI: Lower discount, can change instance type
  - Scheduled RI: Reserved for specific time windows
- **Use when**: Steady-state, predictable workloads
- **Payment options**: All upfront, partial upfront, no upfront

**Savings Plans**
- Commitment to consistent compute usage ($/hour)
- Up to 72% discount
- More flexible than Reserved Instances
- **Types**:
  - Compute Savings Plan: Most flexible (any instance, any region)
  - EC2 Instance Savings Plan: Specific instance family
- **Use when**: Flexible workloads, need portability across instance types

**Spot Instances**
- Request unused EC2 capacity
- Up to 90% discount vs. on-demand
- Can be interrupted with 2-minute warning
- **Use when**: Fault-tolerant, flexible workloads
- **Use cases**: Batch jobs, big data, CI/CD, stateless applications
- **Not suitable for**: Databases, critical applications

**Dedicated Hosts**
- Physical server fully dedicated to your use
- Server-bound software licenses (Oracle, SQL Server)
- Compliance requirements
- Most expensive option

**Dedicated Instances**
- Instances run on hardware dedicated to single customer
- May share hardware with other instances from same account
- No control over instance placement

### 5. EC2 Storage Options

**Amazon EBS (Elastic Block Store)**
- Persistent block storage volumes
- Attached to EC2 instances via network
- Survives instance termination (if configured)
- **Types**:
  - **gp3/gp2**: General purpose SSD
  - **io2/io1**: Provisioned IOPS SSD (high performance)
  - **st1**: Throughput optimized HDD
  - **sc1**: Cold HDD (lowest cost)
- **Features**:
  - Snapshots to S3
  - Encryption support
  - Can detach/reattach to different instances
  - Multi-Attach for io2 (shared storage)

**Instance Store**
- Ephemeral (temporary) storage
- Physically attached to host computer
- Very high IOPS and throughput
- Data lost when instance stops/terminates
- **Use cases**: Temporary data, cache, buffers

**Amazon EFS (Elastic File System)**
- Network file system (NFS)
- Can be mounted on multiple EC2 instances simultaneously
- Scales automatically
- **Use cases**: Shared file storage, content repositories

**Amazon FSx**
- Fully managed third-party file systems
- **FSx for Windows File Server**: Windows-native
- **FSx for Lustre**: High-performance computing

### 6. EC2 Networking

**Elastic Network Interface (ENI)**
- Virtual network card
- Has private IP, optional public IP
- Security groups attached to ENI
- Can be moved between instances

**Elastic IP Address (EIP)**
- Static public IPv4 address
- Remains with you until released
- Can be reassigned to different instances
- **Cost**: Free when attached to running instance, charged when not in use

**Placement Groups**
Logical grouping of instances for specific purposes:
- **Cluster**: Low latency, high throughput (same AZ)
- **Spread**: Instances on different hardware (up to 7 per AZ)
- **Partition**: Divides instances into partitions (different racks)

**Enhanced Networking**
- Higher bandwidth, lower latency
- **Elastic Network Adapter (ENA)**: Up to 100 Gbps
- **Elastic Fabric Adapter (EFA)**: For HPC and ML workloads

### 7. EC2 Security

**Security Groups**
- Virtual firewalls for EC2 instances
- Control inbound and outbound traffic
- **Stateful**: Return traffic automatically allowed
- Can reference other security groups
- Default: All inbound denied, all outbound allowed

**Key Pairs**
- Public-key cryptography for SSH/RDP access
- AWS stores public key
- You store private key securely
- Required for Linux instance access

**IAM Roles for EC2**
- Grant permissions to applications running on EC2
- No need to embed credentials in code
- Temporary credentials automatically rotated
- Best practice over using access keys

### 8. EC2 Auto Scaling

**Components:**

**Launch Template/Configuration**
- Specifies instance configuration (AMI, instance type, security groups)
- Launch template is newer and recommended

**Auto Scaling Group (ASG)**
- Collection of EC2 instances treated as logical grouping
- Maintains desired number of instances
- Spans multiple AZs for high availability

**Scaling Policies**
- **Target Tracking**: Maintain specific metric (e.g., 50% CPU)
- **Step Scaling**: Scale based on metric thresholds
- **Simple Scaling**: Single adjustment based on alarm
- **Scheduled Scaling**: Scale at specific times
- **Predictive Scaling**: ML-based forecasting

**Health Checks**
- EC2 status checks
- ELB health checks
- Custom health checks
- Automatically replaces unhealthy instances

### 9. EC2 Monitoring

**CloudWatch Metrics**
- **Basic monitoring**: 5-minute intervals (free)
- **Detailed monitoring**: 1-minute intervals (additional cost)
- **Default metrics**: CPU, Network, Disk, Status checks
- **Custom metrics**: Memory, disk space (requires CloudWatch agent)

**Status Checks**
- **System status checks**: AWS infrastructure issues
- **Instance status checks**: Software/OS issues

**CloudWatch Logs**
- Collect logs from applications
- Requires CloudWatch Logs agent

**CloudWatch Alarms**
- Alert on metric thresholds
- Trigger Auto Scaling actions
- SNS notifications

### 10. EC2 Pricing Components

**What you pay for:**
- **Instance hours**: Based on instance type and size
- **Data transfer**: 
  - IN: Free
  - OUT to internet: Charged per GB
  - Between regions: Charged
  - Within same AZ: Free (usually)
- **Storage**: EBS volumes and snapshots
- **Elastic IPs**: When not attached to running instance
- **Load Balancers**: Per hour + data processed
- **Additional**: EBS-optimized instances, enhanced networking

---

## AWS Lambda

### What is Lambda?
AWS Lambda is a **serverless compute service** that runs code in response to events without provisioning or managing servers. You only pay for the compute time consumed.

Think of it as: **Code that runs on-demand, automatically scales, and you only pay when it executes**

---

## Lambda Core Concepts

### 1. Lambda Function
A piece of code packaged with its configuration and dependencies

**Function Components:**
- **Function code**: Your application logic
- **Handler**: Entry point for execution
- **Runtime**: Execution environment (Python, Node.js, Java, etc.)
- **Configuration**: Memory, timeout, environment variables
- **IAM Role**: Permissions for the function

### 2. Supported Runtimes

**Managed Runtimes:**
- **Node.js**: 18.x, 20.x
- **Python**: 3.9, 3.10, 3.11, 3.12
- **Java**: 8, 11, 17, 21
- **Go**: 1.x
- **.NET**: 6, 8
- **Ruby**: 3.2, 3.3

**Custom Runtimes:**
- Runtime API allows any programming language
- Use Lambda Layers for custom runtimes

### 3. Event Sources (Triggers)

Lambda functions execute in response to events:

**AWS Services:**
- **API Gateway**: HTTP/REST API requests
- **S3**: Object creation/deletion
- **DynamoDB**: Stream records (data changes)
- **SNS**: Topic messages
- **SQS**: Queue messages
- **CloudWatch Events/EventBridge**: Scheduled or event-driven
- **Kinesis**: Stream processing
- **CloudWatch Logs**: Log processing
- **Cognito**: User authentication events
- **ALB**: Application Load Balancer requests

**Direct Invocation:**
- AWS SDK
- AWS CLI
- Lambda Console

### 4. Invocation Models

**Synchronous (Request-Response)**
- Client waits for response
- Example: API Gateway, direct invocation
- Error handling by caller
- Timeout up to 15 minutes

**Asynchronous**
- Lambda queues the event and returns immediately
- Example: S3, SNS, CloudWatch Events
- Built-in retries (2 times by default)
- Dead Letter Queue (DLQ) for failed events

**Event Source Mapping (Polling)**
- Lambda polls the source for records
- Example: SQS, Kinesis, DynamoDB Streams
- Lambda manages polling and batching
- Concurrent executions based on batch size

### 5. Lambda Function Configuration

**Memory Allocation**
- Range: 128 MB to 10,240 MB (10 GB)
- CPU power proportional to memory
- More memory = more CPU = faster execution
- Price increases with memory

**Timeout**
- Range: 1 second to 15 minutes (900 seconds)
- Default: 3 seconds
- Function stops if timeout exceeded

**Environment Variables**
- Key-value pairs for configuration
- Can be encrypted with KMS
- Accessible in function code

**Concurrency Settings**
- **Reserved concurrency**: Guarantees capacity
- **Provisioned concurrency**: Pre-warmed instances
- **Unreserved concurrency**: Shared pool (default)

**Execution Role (IAM)**
- Permissions for accessing AWS services
- AWSLambdaBasicExecutionRole minimum (CloudWatch Logs)
- Grant least privilege permissions

### 6. Lambda Layers

Reusable components shared across functions:
- **Libraries and dependencies**
- **Custom runtimes**
- **Configuration files**
- **Shared code**

**Benefits:**
- Reduce deployment package size
- Share code between functions
- Separate core logic from dependencies
- Up to 5 layers per function

### 7. Lambda Execution Environment

**Lifecycle:**

1. **INIT Phase** (Cold Start)
   - Download code
   - Start runtime
   - Run initialization code (outside handler)
   - Takes 100ms - several seconds

2. **INVOKE Phase**
   - Execute handler function
   - Billed for this time

3. **SHUTDOWN Phase**
   - Environment recycled after inactivity

**Cold Start vs. Warm Start:**
- **Cold start**: First invocation or after idle period
- **Warm start**: Execution environment reused
- **Optimization**: Use provisioned concurrency for critical functions

**Execution Context Reuse:**
```python
# Runs once per container (initialization)
import json
db_connection = create_connection()  # Reused

def lambda_handler(event, context):
    # Runs on every invocation
    result = db_connection.query()
    return result
```

### 8. Lambda Limits and Quotas

**Hard Limits (Cannot be Changed):**
- Deployment package: 50 MB (zipped), 250 MB (unzipped)
- /tmp storage: 512 MB to 10,240 MB
- Execution timeout: 15 minutes maximum
- Environment variables: 4 KB total
- Layers: 5 per function, 250 MB total unzipped

**Soft Limits (Can Request Increase):**
- Concurrent executions: 1,000 per region (default)
- Function and layer storage: 75 GB per region

### 9. Lambda Pricing

**What You Pay For:**

**Requests:**
- First 1 million requests/month: FREE
- After: $0.20 per 1 million requests

**Duration:**
- Free tier: 400,000 GB-seconds/month
- Charged per GB-second
- Calculation: Memory (GB) × Execution time (seconds)

**Example:**
```
Function with 512 MB memory, runs 1 second
= 0.5 GB × 1 second = 0.5 GB-seconds

If it runs 1 million times:
= 500,000 GB-seconds
= Within free tier (400,000 free + some paid)
```

**Additional Costs:**
- Data transfer out to internet
- CloudWatch Logs storage
- Other AWS services called

### 10. Lambda Best Practices

**Performance:**
- Minimize deployment package size
- Reuse execution context (connections, clients)
- Use environment variables for configuration
- Allocate sufficient memory (more = faster CPU)
- Avoid recursive code
- Use provisioned concurrency for latency-sensitive apps

**Security:**
- Follow least privilege for IAM roles
- Don't embed credentials in code
- Use Secrets Manager or Parameter Store
- Enable VPC only when needed (adds cold start time)
- Encrypt environment variables with KMS
- Use Lambda layers for shared sensitive data

**Cost Optimization:**
- Right-size memory allocation
- Set appropriate timeouts
- Use reserved concurrency carefully
- Clean up unused functions
- Monitor with CloudWatch insights

**Error Handling:**
- Implement idempotent functions
- Use DLQ for asynchronous invocations
- Set up CloudWatch alarms
- Log meaningful error messages
- Retry with exponential backoff

**Development:**
- Use Lambda function versions
- Implement aliases (dev, staging, prod)
- Use SAM or Serverless Framework
- Test locally with SAM CLI
- Implement CI/CD pipelines

### 11. Lambda Use Cases

**Perfect For:**
- **Event-driven processing**: S3 uploads, DynamoDB changes
- **API backends**: With API Gateway
- **Real-time file processing**: Image/video thumbnails
- **Stream processing**: Kinesis, DynamoDB Streams
- **Scheduled tasks**: CloudWatch Events cron jobs
- **Webhooks**: Third-party service integrations
- **IoT backends**: Process device data
- **Automation**: Infrastructure automation scripts
- **Chatbots**: Lex or Slack bot backends

**Not Ideal For:**
- Long-running processes (> 15 minutes)
- Applications requiring persistent connections
- High-frequency, low-latency needs (use EC2)
- Applications with large dependencies (consider containers)
- Stateful applications (Lambda is stateless)

### 12. Lambda Advanced Features

**Destinations**
- Route execution results to other services
- Success and failure destinations
- Supported: SQS, SNS, Lambda, EventBridge

**Lambda Extensions**
- Augment functions with monitoring, observability, security tools
- Run in separate process alongside function
- External and internal extensions

**Lambda Container Images**
- Package functions as container images (up to 10 GB)
- Use familiar container tooling
- Maintain consistency across environments

**Function URLs**
- Built-in HTTPS endpoint for Lambda
- No need for API Gateway for simple use cases
- Supports IAM auth or public access

**SnapStart (Java)**
- Improves cold start performance
- Takes snapshot of initialized execution environment
- Available for Java 11 and later

---

## EC2 vs Lambda Comparison

| Aspect | EC2 | Lambda |
|--------|-----|--------|
| **Management** | You manage servers | AWS manages infrastructure |
| **Scaling** | Manual or Auto Scaling setup | Automatic, instant |
| **Pricing** | Pay for running time | Pay per invocation + duration |
| **Execution Time** | Unlimited | Max 15 minutes |
| **Control** | Full OS and application control | Limited to function code |
| **State** | Can be stateful | Stateless |
| **Startup Time** | Minutes to provision | Milliseconds (warm) to seconds (cold) |
| **Use Cases** | Long-running, complex apps | Event-driven, short tasks |
| **Minimum Cost** | Always paying when running | Pay only when executing |
| **Idle Cost** | Charged even when idle | Zero cost when not running |

---

## When to Use What?

### Use EC2 When:
- ✅ Application runs continuously
- ✅ Need full control over OS
- ✅ Long-running processes
- ✅ Specific hardware requirements
- ✅ Applications with persistent connections
- ✅ Legacy applications
- ✅ More cost-effective for steady workloads

### Use Lambda When:
- ✅ Event-driven architecture
- ✅ Short, stateless operations
- ✅ Variable or unpredictable traffic
- ✅ Want to minimize operational overhead
- ✅ Microservices architecture
- ✅ Rapid scaling requirements
- ✅ Pay-per-use is more economical

### Hybrid Approach:
Many architectures use **both**:
- EC2 for core application servers
- Lambda for event processing, automation, API backends
- Example: EC2 runs main app, Lambda processes uploaded files

---

## Practical Examples

### EC2 Example: Web Application
```
Architecture:
- Multi-AZ Auto Scaling group
- Application Load Balancer
- RDS database (Multi-AZ)
- S3 for static assets
- CloudFront for CDN

Why EC2?
- Continuous operation
- Complex application logic
- Database connections
- Predictable steady-state traffic
```

### Lambda Example: Image Processing
```
Architecture:
- User uploads to S3
- S3 triggers Lambda function
- Lambda creates thumbnail
- Stores thumbnail in S3
- Updates DynamoDB metadata

Why Lambda?
- Event-driven (S3 upload)
- Short processing time
- Sporadic usage
- Auto-scaling
- No idle server costs
```

---
