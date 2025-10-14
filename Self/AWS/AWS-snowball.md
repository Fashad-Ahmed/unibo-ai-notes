# AWS Snowball Notes

## Overview
AWS Snowball is a physical data transfer service that helps move large amounts of data into and out of AWS using secure, rugged devices shipped directly to your location.

## Key Concepts

### What is Snowball?
- Physical storage device provided by AWS
- Used for petabyte-scale data transfers
- Addresses challenges of large-scale data migration over networks
- Alternative to transferring data over the internet

### Why Use Snowball?
- **Large data volumes**: Transferring terabytes or petabytes of data
- **Limited bandwidth**: Network bandwidth is limited or expensive
- **Time constraints**: Network transfers would take too long
- **Cost efficiency**: More economical than high-speed internet transfers for large datasets

## Snowball Device Types

### Snowball Edge Storage Optimized
- 80 TB of usable storage
- 40 vCPUs and 80 GiB of memory
- 1 TB SSD for block volumes
- Local compute capabilities with EC2 and Lambda

### Snowball Edge Compute Optimized
- 42 TB of usable storage
- 52 vCPUs and 208 GiB of memory
- Optional GPU for machine learning
- Enhanced compute for edge processing

## Key Features

### Security
- 256-bit encryption (managed via AWS KMS)
- Tamper-resistant enclosure
- Trusted Platform Module (TPM)
- End-to-end tracking with E Ink shipping label

### Durability
- Ruggedized to withstand shipping
- Weather-resistant
- Secure, protective case

### Integration
- S3-compatible endpoint
- AWS CLI support
- SDK integration
- File interface option

## Use Cases
- **Data center migration**: Moving entire data centers to AWS
- **Content distribution**: Shipping media files and large datasets
- **Backup and disaster recovery**: Bulk backup transfers
- **Manufacturing**: Collecting and processing data at edge locations
- **Remote locations**: Data collection where connectivity is limited

## Workflow

1. **Request device**: Order Snowball through AWS Console
2. **Receive device**: AWS ships device to your address
3. **Connect and transfer**: Connect device to your network and copy data
4. **Ship back**: Return device to AWS using prepaid shipping label
5. **Data import**: AWS transfers data to your S3 buckets
6. **Verification**: Receive confirmation and verify data integrity

## Pricing Considerations
- Service fee per job
- Extra day charges beyond included usage period
- Data transfer into AWS is typically free
- Data transfer out of AWS incurs charges
- Shipping costs included in service fee

## Related Services
- **Snowball Edge**: Enhanced compute and storage capabilities
- **Snowmobile**: Exabyte-scale transfer (45-foot shipping container)
- **Snowcone**: Smallest device (8 TB) for edge computing and transfer
- **AWS DataSync**: Online data transfer service
- **AWS Transfer Family**: Managed file transfer service

## Best Practices
- Plan data organization before transfer
- Use parallel transfers when possible
- Test workflow with smaller dataset first
- Monitor transfer progress
- Keep device in controlled environment
- Maintain chain of custody documentation

## Limitations
- Physical device must be shipped (time required)
- Geographic availability varies
- Import/export restrictions in some countries
- Device availability subject to AWS supply
- 


-----------




## Steps:

When requesting a device there are several steps including configuring: Job type, Compute and storage, Features and options, as well as Security, shipping and notification preferences. We'll be reviewing the first two steps in the process.

Provide a name for the data transfer job, such as 'MyFirstImport'
For job type, we'll set it to Import into Amazon S3.
Navigate to Step 2, Compute and Storage. In this section is where you would typically configure what type of device you want based on factors such as Compute (CPUs/GPUs), Memory, Storage (HDD) and Storage (SDD).
Further down the page, you can also select the destination you would like your data transferred to. You can select an already available bucket in your organization, alternatively you can create a new one.
Now we can cancel out of the Snowball job creation process, and look at other services.

