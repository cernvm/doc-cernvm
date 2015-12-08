# Running in Vagrant

[Vagrant](https://www.vagrantup.com/) is a tool that facilitates the instantiation of reproducible and portable development environments using virtual machines.  CernVM is available as a vagrant compatible image ("Vagrant box"), which is a slightly adjusted CernVM VirtualBox image.

The `vagrant` utility is available for Windows, OS X, and Linux.

In order to start a CernVM under Vagrant, download the CernVM image for Vagrant and run

    vagrant box add --name CernVM <cernvm image>.box

Browse into your developemnt directory (or another directory of your choice) and run

    vagrant init CernVM

where `CernVM` is the name from the `box add` command.  The `init` command places an initial `Vagrantfile` into the working directory.  In order to start CernVM and to connect to it through ssh, run from this directory

    vagrant up
    vagrant ssh

Inside the virtual machine, you'll find the host directory under /vagrant.
