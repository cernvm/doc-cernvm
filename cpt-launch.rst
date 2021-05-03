.. _sct_launch:

CernVM Launch
=============

**Note**: CernVM Launch does currently not work with VirtualBox 6.1 on Windows. We are working on a fix. Please use VirtualBox 6.0 for the time being.

The ``cernvm-launch`` utility is a single binary for `Windows <https://ecsft.cern.ch/dist/cernvm/launch/bin/Win/cernvm-launch.exe>`_, `Linux <https://ecsft.cern.ch/dist/cernvm/launch/bin/Linux/cernvm-launch>`_, and `Mac <https://ecsft.cern.ch/dist/cernvm/launch/bin/Mac/cernvm-launch>`_ that creates, lists, and destroys (interactive) CernVMs on `VirtualBox <https://www.virtualbox.org/>`_. It works similar to the vagrant and docker command line utilities. It is meant to be used for interactive (graphical) CernVM instances on a local workstation or laptop.

Installation
------------

As a one time preparation you need to:

  * Install `VirtualBox <https://www.virtualbox.org/>`_.
  * `Download the CernVM-Launch binary <https://ecsft.cern.ch/dist/cernvm/launch/bin/>`_ for your operating system and put it in your ``PATH`` environment (see below).

Once installed, you can manage CernVM instances using different ":ref:`context <sct_context>`" ASCII files, which you can store on your computer.

The installation process depends on the platform. For instructions how to install VirtualBox, please visit the `official VirtualBox page <https://www.virtualbox.org/wiki/Downloads>`_.


Linux/Mac Installation
~~~~~~~~~~~~~~~~~~~~~~

Run the following commands in your terminal:

::

    # Download
    if [ "x$(uname -s)" = "xLinux" ]; then
      curl -o cernvm-launch https://ecsft.cern.ch/dist/cernvm/launch/bin/Linux/cernvm-launch
    else
      curl -o cernvm-launch https://ecsft.cern.ch/dist/cernvm/launch/bin/Mac/cernvm-launch
    fi
    chmod +x cernvm-launch  # make it executable
    # As root user, place it in a directory from the $PATH environment
    sudo cp cernvm-launch /usr/local/bin

You can pick a different directory from your ``$PATH`` environment. Use ``echo $PATH`` to see all possible directories.


Windows
~~~~~~~

Download the `cernvm-launch executable <https://ecsft.cern.ch/dist/cernvm/launch/bin/Win/cernvm-launch.exe>`_. Open a Windows prompt as an Administrator

  * Click the Start icon
  * Type ``cmd``
  * Right-click on "cmd.exe" and click "Run as administrator"

Go to the directory where you have the downloaded binary, e.g.

::

    cd C:\Users\sftnight\Downloads

From there, copy the binary in a directory, which is a default path for executable, e.g.

::

    copy cernvm-launch.exe C:\Windows

You can see your path directories with ``echo %PATH%``.

Usage
-----

The ``cernvm-launch`` executable includes an embedded help page:

::

    $ cernvm-launch -h
    Usage: cernvm-launch OPTION
    OPTIONS:
	           create [--no-start] [--name MACHINE_NAME] [--cpus NUM] [--memory NUM_MB] [--disk NUM_MB]
	                  [--iso PATH] [--sharedFolder PATH] [USER_DATA_FILE] [CONFIGURATION_FILE]
		                  Create a machine with default or specified user data.
	           destroy [--force] MACHINE_NAME	Destroy an existing machine.
	           import [--no-start] [--name MACHINE_NAME] [--memory NUM_MB] [--disk NUM_MB]
	                  [--cpus NUM] [--sharedFolder PATH] OVA_IMAGE_FILE [CONFIGURATION_FILE]
		                  Create a new machine from an OVA image.
	           list [--running] [MACHINE_NAME]	List all existing machines or a detailed info about one.
	           pause MACHINE_NAME	Pause a running machine.
	           ssh [user@]MACHINE_NAME	SSH into an existing machine.
	           start MACHINE_NAME	Start an existing machine.
	           stop MACHINE_NAME	Stop a running machine.
	           -v, --version		Print version.
	           -h, --help		Print this help message.
 
The most important argument when creating the virtual machine is the ``USER_DATA_FILE`` which defines the machine contextualization, i.e. all the major settings, including the repositories to be mounted, the users, the services to be started and the flavour of the machine. A useful collection of ``contexts`` used in quite different situations is publicly available on `_GitHub <https://github.com/cernvm/public-contexts>`_.

Example
~~~~~~~

The following creates a CMS VM to be used for 2011 open data: 

::

    $ cernvm-launch create --name cms-test --cpus 2 --memory 4096 --disk 20000 cms-opendata-2011.context
    Using user data file: cms-opendata-2011.context
    Parameters used for the machine creation:
	   name: cms-test
	   cpus: 2
	   memory: 4096
	   disk: 20000
	   cernvmVersion: 2021.05-1
	   sharedFolder: /Users/ganis

The machine features 2 cores, 4 GB RAM and 20 GB hard drive. The local ``HOME`` folder is shared ``R/W`` and
available as a mount point under ``/mnt`` .

At any moment the existing VMs can be checked with the ``list`` sub-command:

::

    $ cernvm-launch list
    cms-test:	CVM: 2021.05-1	port: 8247

which also shows the internal port associsated with the VM . The ``ssh`` sub-command allows to sonnect to the machine:

::

    $ cernvm-launch ssh cms-test
    Username: cms-opendata
    The authenticity of host '[127.0.0.1]:8247 ([127.0.0.1]:8247)' can't be established.
    ECDSA key fingerprint is SHA256:AV6DFteBe7EcDCijcsdFcU6K9f5FjKKtoEWFZEhdvCA.
    Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
    Warning: Permanently added '[127.0.0.1]:8247' (ECDSA) to the list of known hosts.
    cms-opendata@127.0.0.1's password:
    [Outer Shell ~]

Passless ssh login can be setup as usual by creating an ``.ssh`` directory and copying in the host public key.
The username can be specified on the command line:

::

    $ cernvm-launch ssh cms-opendata@cms-test
    Last login: Mon May  3 15:20:37 2021 from gateway

Display settings should be automaticaly transferred (as a simple test, running ``xterm`` should open a terminal into
an X window in the host screen).

The shared folder is available under ``/mnt/shared/cms-test_sf``:

::

    [Outer Shell ~] df -h
    Filesystem                Size  Used Avail Use% Mounted on
    /dev/disk/by-label/UROOT   20G  532M   18G   3% /mnt/.rw
    /dev/fuse                 2.0G  352M  1.7G  18% /mnt/.ro
    root                       20G  532M   18G   3% /
    tmpfs                     2.0G  9.6M  2.0G   1% /run
    devtmpfs                  2.0G     0  2.0G   0% /dev
    tmpfs                     2.0G     0  2.0G   0% /dev/shm
    tmpfs                     2.0G     0  2.0G   0% /sys/fs/cgroup
    cms-test_sf               932G  605G  328G  65% /media/sf_cms-test_sf
    cvmfs2                     20G   46M   20G   1% /cvmfs/cvmfs-config.cern.ch
    cvmfs2                     20G   46M   20G   1% /cvmfs/cms.cern.ch
    cms-test_sf               932G  605G  328G  65% /mnt/shared/cms-test_sf
    tmpfs                     394M  4.0K  394M   1% /run/user/1000
    
Files can also be copied to the VM using ``scp`` and the connection port:

::

    $ scp -P 8247 sample.txt cms-opendata@localhost:~/
    sample.txt                                                             100%    7     4.6KB/s   00:00

Th VM is destroyed by the ``destroy`` sub-command:

::

    $ cernvm-launch destroy cms-test
    The machine 'cms-test' is running, do you want do destroy it? [y/N]: y
    $ cernvm-launch list

