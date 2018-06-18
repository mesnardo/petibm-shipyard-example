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

```
> shipyard pool add --configdir config
> az storage directory create --name snake --share-name myfileshare --account-name <account-name>
> az storage file upload-batch --source snake --destination myfileshare/snake --account-name <account-name>
> shipyard jobs add --configdir config
> shipyard jobs del --configdir config
> shipyard pool del --configdir config
> az storage file download-batch --source myfileshare/snake --destination snake-output --account-name <account-name>
```
