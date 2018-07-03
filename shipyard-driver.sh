#!/usr/bin/env bash
# Provision a pool, ingress data, run a job,
# and delete job and pool once the job is completed.
# cli: ./shipyard-driver.sh

read -p "Enter configuration directory: " configdir
export SHIPYARD_CONFIGDIR=$configdir
echo -n "Password:"
read -s password
export SHIPYARD_AAD_PASSWORD=$password
echo
read -p "Enter directory for log files (press enter to use ./logs): " logdir
logdir=${logdir:-"logs"}
mkdir -p $logdir

shipyard --version > $logdir/version.log 2>&1
echo "Provisioning pool of compute nodes..."
shipyard pool add --yes > $logdir/pool-add.log 2>&1
echo "Ingressing input data..."
shipyard data ingress > $logdir/data-ingress.log 2>&1
echo "Submitting job..."
shipyard jobs add > $logdir/jobs-add.log 2>&1
echo "Polling job until task is complete..."
shipyard jobs tasks list --poll-until-tasks-complete > $logdir/jobs-monitor.log 2>&1
echo "Deleting job..."
shipyard jobs del --yes > $logdir/jobs-del.log 2>&1
echo "Deleting pool..."
shipyard pool del --yes > $logdir/pool-del.log 2>&1

unset SHIPYARD_CONFIGDIR
unset SHIPYARD_AAD_PASSWORD
echo "Done."
