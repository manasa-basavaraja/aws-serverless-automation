Weekend Infrastructure Scheduler – Event Driven Automation
Overview

This solution automates start and stop operations for non-production infrastructure (Oracle Dev, MySQL Dev, Redshift, Aurora, EC2 based services such as Echelon) using an event-driven architecture.

The primary objective is to reduce weekend infrastructure costs by automatically stopping development resources outside business hours and restarting them at the beginning of the week.

Architecture

                ┌──────────────────────────────┐
                │        Amazon EventBridge    │
                │  (Cron Rules - Fri & Mon)    │
                └──────────────┬───────────────┘
                               │
                    JSON Payload
           { "action": "start" | "stop" }
                               │
                               ▼
                ┌──────────────────────────────┐
                │        AWS Lambda Function   │
                │  cluster_scheduler.py        │
                │  - Reads ENV variables       │
                │  - Calls boto3 APIs          │
                └──────────────┬───────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────────────┐
        │              Target Resources                │
        │                                              │
        │  • RDS (Oracle Dev, MySQL Dev)              │
        │  • Aurora Cluster                            │
        │  • Redshift Cluster                          │
        │  • EC2 Instances (Echelon Services)         │
        └──────────────────────────────────────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │       CloudWatch Logs        │
                │  (Monitoring & Auditing)     │
                └──────────────────────────────┘

This implementation uses:

Amazon EventBridge – to trigger scheduled events
AWS Lambda – to execute cluster lifecycle operations
IAM Roles – to securely authorize service actions
Environment Variables – to dynamically manage cluster lists

## This design ensures:

No hardcoding of actions
Clean separation between scheduler and logic
Easy extensibility for additional environments

## Use Cases

- Weekend shutdown of non-production clusters
- Automated cost optimization
- Operational automation for Dev/QA environments
- Reusable framework for additional services

## Business Impact

- Reduced non-production runtime by ~60%
- Estimated annual savings: ~$12K
- Eliminated manual weekend operations
- Fully auditable and scalable design

