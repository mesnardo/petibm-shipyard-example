#!/bin/bash

SIMULATION_DIR=$1

source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

# get number of nodes
IFS=',' read -ra HOSTS <<< "$AZ_BATCH_HOST_LIST"
nodes=${#HOSTS[@]}
echo "Number of nodes: $nodes"
echo "Hosts: $AZ_BATCH_HOST_LIST"
# number of processes per node
ppn=2
echo "Number of processes per node to use: $ppn"
# number of processes
np=$(($nodes * $ppn))
echo "Total number of processes: $np"

# get number of GPUs on machine
ngpusmax=`nvidia-smi -L | wc -l`
echo "Number of GPU devices available on each node: $ngpusmax"
# number of GPUs to use per node
CUDA_VISIBLE_DEVICES=0,1
IFS=',' read -ra GPUS <<< "$CUDA_VISIBLE_DEVICES"
ngpus=${#GPUS[@]}
echo "Number of GPU devices per node to use: $ngpus ($CUDA_VISIBLE_DEVICES)"

echo "PATH: $PATH"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"

mpirun -np $np -ppn $ppn -host $AZ_BATCH_HOST_LIST \
  -genv CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
  petibm-decoupledibpm \
  -directory $SIMULATION_DIR \
  -log_view ascii:$SIMULATION_DIR/log.out \
  -malloc_log \
  -memory_view \
  -options_left
