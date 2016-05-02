# CernVM as a Docker Container

The CernVM docker container resembles the µCernVM idea in docker.  It consists mainly of a busybox and the [parrot](http://ccl.cse.nd.edu/software/parrot) sandboxing tool.  The rest of the operating system is loaded on demand.

Alternatively, it is possible to bind mount the cvmfs operating system repository into the docker container, and then the container will
automatically use this instead of parrot.

## Limitations of the CernVM Docker Container

The CernVM docker container is a runtime environment only.  It can be used to start arbitrary commands "dockerized" in CernVM.  Due to its internal mechanis, it cannot be used, however, as a base image to create derived Docker containers, e.g. with a `Dockerfile`.

## Importing and Running the Container

In order to import the image, ensure that the docker service is running and execute

    cat <CernVM Docker tarball> | docker import - my_cernvm

In order to start an interactive shell, run

    docker run -it my_cernvm /init

The initial command always needs to be `/init`, but any other command can be appended, for instance

    docker run -it my_cernvm /init ls -lah

In case CernVM-FS is mounted on the docker host, it is possible to help the container and bind mount the operating system repository like

    docker run -v /cvmfs/cernvm-prod.cern.ch:/cvmfs/cernvm-prod.cern.ch ...

In this case, there is no Parrot environment.  Every repository that should be available in the docker container needs to be mapped with another `-v ...` parameter.

The image can be further contextualized by environment variables.  To
turn on more verbose output:

    docker run -e CERNVM_DEBUG=1 -it ...

To use another operating system provided by CernVM-FS:

    docker run -e CERNVM_ROOT=/cvmfs/cernvm-sl7.cern.ch/cvm4 -it ...

or

    docker run -e CERNVM_ROOT=/cvmfs/cernvm-slc5.cern.ch/cvm3 -it ...

or

    docker run -e CERNVM_ROOT=/cvmfs/cernvm-slc4.cern.ch/cvm3 -it ...

Standard LHC cvmfs repositories are present by default, other repositories can be added with

    docker run -e PARROT_CVMFS_REPO=" \
      <REPONAME>:url=<STRATUM1-URL>,pubkey=/UCVM/keys/<KEYNAME> \
      <REPONAME>: ..."

The corresponding public key needs to be stored in the container under
/UCVM/keys first.