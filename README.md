# Running PetIBM on Microsoft Azure with Azure Batch and Batch Shipyard

---

## Dependencies

- PetIBM (0.3.1)
- Azure-CLI (2.0.37)
- Batch Shipyard (3.4.0)

---

## Docker image

Dockerhub: `mesnardo/petibm:0.3.1-GPU-IntelMPI-ubuntu`

The Dockerfile is also provided in the folder `docker`.

---

## Command lines

Login your device and setup your subscription:
```
az login
az account set --subscription <subscription name or id>
```

Create a resource group (`snake-rg`) in the East US region (`eastus`):
```
az group create --name snake-rg --location eastus
```

Create an Azure Storage account (`snake2storage`) in the resource group in the East US region:
```
az storage account create --name snake2storage --resource-group snake-rg --sku Standard_LRS --location eastus
```

Create an Azure Batch account (`snake2batch`) in the resource group:
```
az batch account create --name snakebatch --resource-group snake-rg --location eastus --storage-account snake2storage
```

Setup the Batch Shipyard configuration files (located in folder `config`):
```
python shipyard-config-setup.py --configdir config --resource-group snake-rg --account-name snake2storage
```

Create Azure Managed disks:
```
shipyard fs disks add --configdir config
```

Create the storage cluster with attached disks:
```
shipyard fs cluster add --configdir config mystoragecluster
```

Create a pool of compute nodes:
```
shipyard pool add --configdir config
```

To upload input data to the storage cluster:
```
rsync -av -e "ssh -i id_rsa_shipyard_remotefs" snake shipyard@snakestoragecluster000.eastus.cloudapp.azure.com:/data/
```

Submit the Azure Batch job:
```
shipyard jobs add --configdir config
```

Once the task completed and the job is finished, delete the job:
```
shipyard jobs del --configdir config
```

Once done with the compute pool, delete it:
```
shipyard pool del --configdir config
```

To download locally the output data from the storage cluster:
```
mkdir output
rsync -av -e "ssh -i id_rsa_shipyard_remotefs" shipyard@snakestoragecluster000.eastus.cloudapp.azure.com:/data/snake output
```

Once done with the remote filesystem, delete the storage cluster:
```
shipyard fs cluster del --delete-data-disks --delete-virtual-network --configdir config mystoragecluster
```
