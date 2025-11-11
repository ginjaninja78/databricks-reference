#!/bin/bash

# This script demonstrates how to manage Databricks clusters using the Databricks CLI.

# --- Configuration ---
CLUSTER_NAME="My-Automated-Cluster"
CLUSTER_JSON_FILE="cluster_definition.json"

# --- Create a Cluster Definition File ---
cat > ${CLUSTER_JSON_FILE} << EOL
{
  "cluster_name": "${CLUSTER_NAME}",
  "spark_version": "13.3.x-scala2.12",
  "node_type_id": "i3.xlarge",
  "num_workers": 2,
  "autotermination_minutes": 60
}
EOL

# --- Create the Cluster ---
echo "Creating cluster: ${CLUSTER_NAME}"
CLUSTER_ID=$(databricks clusters create --json-file ${CLUSTER_JSON_FILE} | jq -r ".cluster_id")
echo "Cluster created with ID: ${CLUSTER_ID}"

# --- Wait for the Cluster to be Running ---
echo "Waiting for cluster to be running..."
databricks clusters get --cluster-id ${CLUSTER_ID} --output JSON | jq -e ".state == \"RUNNING\""

# --- Get Cluster Info ---
echo "Getting cluster info..."
databricks clusters get --cluster-id ${CLUSTER_ID}

# --- Stop the Cluster ---
# echo "Stopping cluster: ${CLUSTER_ID}"
# databricks clusters permanent-delete --cluster-id ${CLUSTER_ID}

echo "Script complete."
