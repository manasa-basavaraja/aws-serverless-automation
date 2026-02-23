# AWS Serverless Infrastructure Automation
#Event-driven automation framework for lifecycle management and cost optimization of non-production AWS infrastructure.

import os
import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize clients
rds = boto3.client("rds")
redshift = boto3.client("redshift")
ec2 = boto3.client("ec2")

def get_env_list(key):
    """
    Reads comma separated values from environment variable
    Returns empty list if not defined
    """
    value = os.environ.get(key, "")
    return [v.strip() for v in value.split(",") if v.strip()]


def handle_rds_instances(action, instances):
    for db in instances:
        try:
            if action == "start":
                logger.info(f"Starting RDS instance: {db}")
                rds.start_db_instance(DBInstanceIdentifier=db)
            elif action == "stop":
                logger.info(f"Stopping RDS instance: {db}")
                rds.stop_db_instance(DBInstanceIdentifier=db)
        except Exception as e:
            logger.error(f"Failed RDS action on {db}: {str(e)}")


def handle_rds_clusters(action, clusters):
    for cluster in clusters:
        try:
            if action == "start":
                logger.info(f"Starting Aurora cluster: {cluster}")
                rds.start_db_cluster(DBClusterIdentifier=cluster)
            elif action == "stop":
                logger.info(f"Stopping Aurora cluster: {cluster}")
                rds.stop_db_cluster(DBClusterIdentifier=cluster)
        except Exception as e:
            logger.error(f"Failed Aurora action on {cluster}: {str(e)}")


def handle_redshift_clusters(action, clusters):
    for cluster in clusters:
        try:
            if action == "start":
                logger.info(f"Resuming Redshift cluster: {cluster}")
                redshift.resume_cluster(ClusterIdentifier=cluster)
            elif action == "stop":
                logger.info(f"Pausing Redshift cluster: {cluster}")
                redshift.pause_cluster(ClusterIdentifier=cluster)
        except Exception as e:
            logger.error(f"Failed Redshift action on {cluster}: {str(e)}")


def handle_ec2_instances(action, instances):
    for instance in instances:
        try:
            if action == "start":
                logger.info(f"Starting EC2 instance: {instance}")
                ec2.start_instances(InstanceIds=[instance])
            elif action == "stop":
                logger.info(f"Stopping EC2 instance: {instance}")
                ec2.stop_instances(InstanceIds=[instance])
        except Exception as e:
            logger.error(f"Failed EC2 action on {instance}: {str(e)}")


def lambda_handler(event, context):
    """
    Expected EventBridge payload:
    {
        "action": "start"
    }
    or
    {
        "action": "stop"
    }
    """

    logger.info(f"Received event: {json.dumps(event)}")

    action = event.get("action", "").lower()

    if action not in ["start", "stop"]:
        return {
            "statusCode": 400,
            "body": "Invalid action. Use 'start' or 'stop'."
        }

    # Environment Variables
    rds_instances = get_env_list("RDS_INSTANCES")
    aurora_clusters = get_env_list("AURORA_CLUSTERS")
    redshift_clusters = get_env_list("REDSHIFT_CLUSTERS")
    ec2_instances = get_env_list("EC2_INSTANCES")

    # Execute actions
    handle_rds_instances(action, rds_instances)
    handle_rds_clusters(action, aurora_clusters)
    handle_redshift_clusters(action, redshift_clusters)
    handle_ec2_instances(action, ec2_instances)

    return {
        "statusCode": 200,
        "body": f"{action.upper()} operation triggered successfully"
    }