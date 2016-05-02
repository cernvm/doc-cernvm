# Running in Vagrant

[Vagrant](https://www.vagrantup.com/) is a tool that facilitates the instantiation of reproducible and portable development environments using virtual machines.  CernVM is available as a vagrant compatible image ("Vagrant box"), which is a slightly adjusted CernVM VirtualBox image.

The `vagrant` utility is available for Windows, OS X, and Linux.

In order to start a CernVM under Vagrant, download the CernVM image for Vagrant and run

    vagrant box add --name CernVM <cernvm image>.box

Adding the box only needs to be done once.  From there you can start multiple VMs that are bound to different directories.  Browse into a source code directory (or another directory of your choice) and run

    vagrant init CernVM

where `CernVM` is the name from the `box add` command.  The `init` command places an initial `Vagrantfile` into the working directory.  In order to start CernVM and to connect to it through ssh, run from this directory

    vagrant up
    vagrant ssh

## Next steps

Inside the virtual machine, you'll find the host directory under /vagrant.  The vagrant VM has the user `vagrant` pre-configured as a main user that is also allowed to run sudo commands.  The vagrant VM provides a usable development environment in most cases.  However, it is not fully contextualized for any particular experiment.

You can start and stop the vagrant VM from the host with

    vagrant halt
    vagrant up

You can remove the VM with

    vagrant destroy

Also remove the `Vagrantfile` and the `.vagrant` directory from the host.

## Shared Folders on Linux Hosts

If mounting the NFS shared folders hangs on Linux, check if a firewall is active and prevents the NFS ports on the hosts to be contacted by the guest.

## SSH on Windows Hosts

On Windows hosts, in addition to vagrant also an `ssh` binary is needed.  You can install git and select to install the git-provided system utilities for a working ssh.
