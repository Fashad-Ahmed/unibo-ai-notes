# The Practical AWS Learning Path 🚀

This guide provides a structured, step-by-step path to learn the foundational services of Amazon Web Services. Each step includes the essential theoretical knowledge and a set of practical, hands-on exercises to build real-world skills.

---

## 🗺️ Table of Contents

1.  [**Step 1: The Foundation & Core Security (IAM)**](#step-1-the-foundation--core-security-iam-)
2.  [**Step 2: The Core Compute Service (EC2)**](#step-2-the-core-compute-service-ec2-)
3.  [**Step 3: Scalable Storage (S3)**](#step-3-scalable-storage-s3-️)
4.  [**Step 4: Networking Your Resources (VPC)**](#step-4-networking-your-resources-vpc-)
5.  [**Step 5: Managed Databases (RDS & DynamoDB)**](#step-5-managed-databases-rds--dynamodb-)
6.  [**Next Steps & Putting It All Together**](#-next-steps--putting-it-all-together)

---

## **Step 1: The Foundation & Core Security (IAM)** 🔑

Before you build anything, you must secure your environment. IAM is the most critical service to master first.

### 🧠 Knowledge To Acquire

-   **What it is:** IAM (Identity & Access Management) is the global service that controls access to AWS resources.
-   **Why it matters:** It allows you to enforce the **Principle of Least Privilege**, ensuring users and applications only have the permissions they absolutely need. **Never use your root account for daily tasks.**
-   **Core Components:**
    -   **Users:** Identities for people or applications.
    -   **Groups:** Collections of users for easier permission management.
    -   **Roles:** Identities with specific permissions that can be temporarily assumed by trusted entities (like an EC2 instance).
    -   **Policies:** JSON documents that define the actual permissions (what actions are allowed or denied on which resources).

### 💻 Hands-On Practice

1.  **Sign up for the AWS Free Tier.**
2.  **Secure your Root User:** Immediately enable **Multi-Factor Authentication (MFA)**.
3.  **Create an IAM Admin User:** Create a new IAM user for yourself and attach the `AdministratorAccess` policy.
4.  **Log In as IAM User:** Log out of your root account and log back in with your new IAM user. **Use this user for everything else.**
5.  **Test Permissions:** Create a second IAM user with a restrictive, read-only policy (e.g., `AmazonS3ReadOnlyAccess`). Log in as that user to see how their access is limited.

---

## **Step 2: The Core Compute Service (EC2)** 💻

This is where you'll run your applications. EC2 provides the virtual servers that are the backbone of many AWS architectures.

### 🧠 Knowledge To Acquire

-   **What it is:** EC2 (Elastic Compute Cloud) provides resizable virtual servers, called **instances**.
-   **Why it matters:** It's the fundamental Infrastructure as a Service (IaaS) offering, giving you complete control over your computing environment.
-   **Core Components:**
    -   **Amazon Machine Image (AMI):** A template (OS + software) used to launch instances.
    -   **Instance Types:** Different configurations of CPU, RAM, and storage (e.g., `t2.micro`).
    -   **Security Groups:** A virtual firewall that controls inbound/outbound traffic for an instance. By default, all inbound traffic is denied.
    -   **Key Pairs:** Used for secure SSH authentication into Linux instances.

### 💻 Hands-On Practice

1.  **Launch an Instance:** From the console, launch an Amazon Linux 2 `t2.micro` instance (it's Free Tier eligible).
2.  **Configure Security Group:** Create a new security group. Add rules to allow `SSH (port 22)` from `My IP` and `HTTP (port 80)` from `Anywhere`.
3.  **Connect to the Instance:** Use an SSH client and the `.pem` key file you downloaded to connect to your instance's public IP address.
4.  **Install a Web Server:** Run the following commands inside your instance via SSH:
    ```bash
    sudo yum update -y
    sudo yum install -y httpd
    sudo systemctl start httpd
    sudo systemctl enable httpd
    ```
5.  **Verify:** Open your web browser and navigate to your instance's public IP address. You should see the Apache test page.
6.  **Clean Up:** Go back to the EC2 console and **terminate** your instance to avoid costs.

---

## **Step 3: Scalable Storage (S3)** 🗄️

S3 is the universal solution for storing files, static assets, backups, and large datasets in the cloud.

### 🧠 Knowledge To Acquire

-   **What it is:** S3 (Simple Storage Service) is a highly durable and scalable **object storage** service.
-   **Why it matters:** It's incredibly cheap, effectively offers infinite storage, and is integrated with nearly every other AWS service. It is NOT a file system to be mounted on an OS.
-   **Core Components:**
    -   **Buckets:** Containers for your data. Bucket names must be **globally unique**.
    -   **Objects:** The files you store, each with a unique key (name).
    -   **Static Website Hosting:** A powerful feature to serve web content directly from S3.

### 💻 Hands-On Practice

1.  **Create a Bucket:** Create a new S3 bucket.
2.  **Upload Files:** Upload a simple `index.html` and an `error.html` file.
3.  **Enable Static Website Hosting:** In the bucket's "Properties" tab, enable this feature and specify your index and error documents.
4.  **Set Public Permissions:** In the "Permissions" tab, add a bucket policy that allows public `GetObject` actions. The console can help generate this for you.
5.  **Access Your Site:** Use the public website endpoint URL provided by S3 to view your live page.

---

## **Step 4: Networking Your Resources (VPC)** 🌐

A VPC provides a private, isolated space in the cloud for your resources, giving you control over security and architecture.

### 🧠 Knowledge To Acquire

-   **What it is:** A VPC (Virtual Private Cloud) is your own virtual network within AWS.
-   **Why it matters:** It's the foundation of network security. It allows you to isolate resources, like databases, from the public internet while keeping web servers accessible.
-   **Core Components:**
    -   **Subnets:** Subdivisions of your VPC's IP range. Can be **public** (with a route to the internet) or **private** (isolated).
    -   **Route Tables:** Control how traffic is routed between subnets and to the internet.
    -   **Internet Gateway (IGW):** The component that connects a VPC to the internet.
    -   **NAT Gateway:** Allows resources in a private subnet to initiate outbound traffic to the internet (e.g., for software updates) while remaining inaccessible from the outside.

### 💻 Hands-On Practice

1.  **Create a Custom VPC:** In the VPC console, use the "VPC and more" wizard to create a VPC with one public and one private subnet across two Availability Zones.
2.  **Launch a Public Instance:** Launch an EC2 instance into your public subnet. Verify you can SSH into it from your computer.
3.  **Launch a Private Instance:** Launch another EC2 instance into your private subnet.
4.  **Test Connectivity:** From your public instance ("bastion host"), try to SSH into the private instance using its private IP address. Confirm you *cannot* SSH into the private instance directly from the internet.

---

## **Step 5: Managed Databases (RDS & DynamoDB)** 🗃️

Let AWS manage the hard work of running databases, so you can focus on your application.

### 🧠 Knowledge To Acquire

-   **RDS (Relational Database Service):** A managed service for **relational databases** like MySQL, PostgreSQL, etc. AWS handles patching, backups, and failover.
-   **DynamoDB (NoSQL):** A fully managed, serverless, key-value **NoSQL database**. It offers single-digit millisecond performance at any scale.

### 💻 Hands-On Practice

1.  **Launch an RDS Database:** Create a Free Tier `db.t2.micro` MySQL RDS instance.
2.  **Secure Placement:** Crucially, place the RDS instance in one of the **private subnets** of the VPC you created in the previous step.
3.  **Configure Security Group:** Create a new security group for the database. Add a rule that allows inbound traffic on `port 3306` (MySQL) *only* from the security group of your public web server instance.
4.  **Connect to it:** SSH into your public EC2 instance, install a MySQL client (`sudo yum install mysql -y`), and use the command line to connect to the database using the endpoint, username, and password provided by RDS.

---

## ✅ Next Steps & Putting It All Together

Congratulations! By completing these steps, you have practiced the core skills of a cloud engineer: **securing, computing, storing, and networking**.

Your next steps should focus on automation and modern application architectures:

-   **Serverless:** Learn **AWS Lambda** and **API Gateway** to run code without managing servers.
-   **Infrastructure as Code (IaC):** Use **AWS CloudFormation** or **Terraform** to define your infrastructure in code, making it repeatable and automated.
-   **Containers:** Explore **Amazon ECS** (Elastic Container Service) or **EKS** (Elastic Kubernetes Service) for deploying containerized applications.
