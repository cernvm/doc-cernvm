02.05.2016: CernVM 3.6
======================

## Overview

CernVM 3 is a virtual machine image based on Scientific Linux 6 combined with a custom, virtualization-friendly Linux kernel.

CernVM 3 is based on the [µCernVM bootloader](http://arxiv.org/abs/1311.2426).  Its outstanding feature is that it does not require a hard disk image to be distributed (hence "micro").  Instead it is distributed as a read-only image of ~20MB containing a Linux kernel and the CernVM-FS client.  The rest of the operating system is downloaded and cached on demand by CernVM-FS.  The virtual machine still requires a hard disk as a persistent cache, but this hard disk is initially empty and can be created instantaneously, instead of being pre-created and distributed.

CernVM 3 comes with a C++11 compiler, a Go compiler, an Erlang interpreter, GNUplot, ROOT, R, octave, LaTeX, scipy and numpy, and many other useful packages.  For distributed computing, CernVM 3 comes with tools such as Condor, Ganglia, Squid, XrootD, Puppet, Parrot and Workqueue/Makeflow, and others.  In order to manage your virtual machines in the cloud, CernVM 3 comes with the cloud management utilities for OpenStack (nova, glance), Amazon EC2 (ec2-... and euca-...), Google Compute Engine (gcutil, gsutil, gcloud), and Microsoft Azure (azure).

If you believe an important package is missing, please let us know!


## Update from CernVM 3.5 and Earlier

In contrast to regular CernVM security updates, this update is a lock-step update that requires both  both the µCernVM bootloader and the operating system to be updated.  In order to update from CernVM 3.5 or earlier run

    sudo cernvm-update -k
    sudo cernvm-update -a

Unlike the CernVM security updates, this is a minor release.  We recommend to use your hypervisor to **make a VM snapshot before you update**.

**Note on docker**: after upgrading from a version < CernVM 3.4, please add your user account manually to the docker group through

    sudo usermod -aG docker <USER NAME>

### Changes to compared to CernVM 3.5
+ Kernel update to 4.1.23
+ AFS update to 1.6.17
+ Add support for vagrant as a host
+ New packages: aspell, gitk, gnuchess, iftop, iotop, jq, libatomic, libcap-devel, links, mod\_fcgid, mod\_gridsite, pandoc, plotutils, python-heatclient, python-sphinx, trickle, valgrind-devel, voms, voms-devel
+ Major version updates: condor (8.0.4 --> ), cctools (3.7.1 --> 5.2.0)
+ Improved speed of the early boot phase
+ Fix occasional data corruption on older pre-SL7 libvirt
+ Disable logwatch cron job
+ Improve integration with glideinWMS
+ Use cvmfs proxy from micro-contextualization
+ Security fixes: firefox, java-1.7.0

### Enforce booting a previous version of CernVM

Booting a previous version of CernVM can be enforced using the following contextualization snippet:

    [ucernvm-begin]
    cvmfs_tag=cernvm-system-<VERSION>
    [ucernvm-end]

The VERSION corresponds to the version of the cernvm-system RPM.  For an interactive virtual machine, hit `<TAB>` in the early boot menu and then `e` to edit the entry.  You can change the `cvmfs_repository_tag` boot parameter from HEAD to VERSION.

Note that previous versions do not contain the latest security fixes.

## Installation

Download the latest images from [our download page](http://cernvm.cern.ch/portal/downloads).  The image is generic and available in different file formats for different hypervisors. The image needs to be contextualized to become either a graphical development VM or a batch virtual machine for the cloud.

Detailed instructions are available for [VirtualBox](http://cernvm.cern.ch/portal/vbprerequisites), [VMware](http://cernvm.cern.ch/portal/vmwprerequisites), [KVM](http://cernvm.cern.ch/portal/kvm), [CERN OpenStack](http://cernvm.cern.ch/portal/openstack), [Amazon EC2](http://cernvm.cern.ch/portal/ec2), [Google Compute Engine](http://cernvm.cern.ch/portal/gce), and [Microsoft Azure](http://cernvm.cern.ch/portal/azure).


## Contextualization

A CernVM needs to be contextualized on first boot.  The process of contextualization assigns a profile to the particular CernVM 3 instance.  For instance, a CernVM can have the profile of a graphical VM used for development on a laptop; applying another context let the CernVM become a worker node in the cloud.

The [CernVM Online portal](https://cernvm-online.cern.ch) lets you define and store VM profiles in one place. Once defined, the VM profiles can quickly be applied to any newly booted CernVM instance using a pairing mechanism on the login prompt.  Please visit the following pages for more information about how to [create new context templates](http://cernvm.cern.ch/portal/online/documentation/create-new-context) and [pair an instance](http://cernvm.cern.ch/portal/online/documentation/pairing-the-instance) with given template.

Also check out the [CernVM Online Marketplace](https://cernvm-online.cern.ch/market/list).

Please find details on the various contextualiztion options on the [contextualization page](http://cernvm.cern.ch/portal/contextualisation).


## Updates and Version Numbers

When booted, CernVM will load the latest available CernVM 3 version and pin itself on this version.  This ensures that your environment stays the same unless you explicitly take action.  Both the µCernVM bootloader and the CernVM-FS provided operating system can be updated using the `cernvm-update` script.  CernVM machines show an update notification in /etc/motd and in the GUI.  The support list will be notified when updates are ready and will post specific instructions for each update.

The CernVM 3 strong version number consists of 4 parts: 3.X.Y.Z.  Major version 3 indicates an Scientific Linux 6 based CernVM.  Minor version X will be changed when there is a significant change in the set of supported features.  "Y" is the bugfix version.  "Z" is the security hotfix version; changes in "Z" don't change the set of packages but provide security fixes for selected packages.


## Next steps

Once booted and contextualized, you can use ssh to connect to your virtual machine. [SSHFS](http://fuse.sourceforge.net/sshfs.html) and shared folders provide you an easy means to exchange files between the host and CernVM.

For storing data and analysis results, we recommend not to use the root partition.  Instead, attach a second hard drive to the virtual machine or use shared folders.  This way, you can move data between virtual machines and the data remains intact even in case the virtual machine ends up in an unsuable state.


## ROOT

In order to start a stand-alone ROOT, click on the tree logo in the middle of the application launcher bar.  In non-graphical mode, use `module load ROOT` to set up the ROOT environemnt.  Afterwards you can just use `root`.  If you want to clean the environment from that particular version of ROOT, use `module unload ROOT`.

## C++11 Compiler

CernVM 3 comes with a C++11 compliant gcc 4.8 compiler that can be used in lieu of the Scientific Linux 6 system compiler.  In order to enable it, run `source /opt/rh/devtoolset-2/enable`.  Apart from gcc 4.8, this also provides matching binutils and a matching gdb and Valgrind.

## Modern LaTeX

By default, CernVM uses the TeXlive 2007 that comes with Scientific Linux 6.  A newer TexLive 2014 distribution is installed in /cvmfs/sft.cern.ch.  In order to activate it, run `module load texlive` (and `module unload texlive` to clean the environment).

## Docker

CernVM can run [docker](https://www.docker.com) containers.  In order to enable docker support, run `sudo /sbin/service docker start`.  In order to enable docker on boot, run `sudo /sbin/chkconfig docker on`.

## Java

By default, CernVM comes with a Java 6 environment.  Java 7 and Java 8 environments are available.  In order to change the default Java version, use `update-alternatives --config java`.

## Single Sign On

You can get a Kerberos token with `kinit`.  With the token, you can login to lxplus and work with subversion repositories without the need to provide a password.  Note that due to DNS issues, this feature is not available in VirtualBox.

## OpenAFS

CernVM has AFS installed but disabled by default. In order to start AFS, you'd need to do

    sudo mkdir /afs
    sudo /sbin/chkconfig afs on
    sudo /sbin/service afs start

Once mounted, you can get an AFS token using `kinit` followed by `aklog`.  In our experience, AFS works poorly behind NAT.  So AFS might be helpful for CernVM on CERN OpenStack but it is not really an option for VMs on the laptop.  Instead, shared folders or `sshfs` can provide an easy way to map directory trees from the host inside the guest.

## Swap Space

By default, CernVM has no swap space enabled.  The following commands creates a 2G swap file

    sudo fallocate -l 2G /mnt/.rw/swapfile
    sudo chmod 0600 /mnt/.rw/swapfile
    sudo mkswap /mnt/.rw/swapfile
    sudo swapon /mnt/.rw/swapfile

If a file /mnt/.rw/swapfile exists, it will picked up automatically on boot as a swap space.  In order to activate a swap space through contextualization, add to your amiconfig user data

    [cernvm]
    swap_size=<SIZE>

where `<SIZE>` can be anything understood by `fallocate -l` or it can be `auto`, in which case CernVM uses 2G/core.

## Makeflow

CernVM 3 supports the [Makeflow](http://www.cse.nd.edu/~ccl/software/makeflow/) workflow engine. Makeflow provides an easy way to define and run distributed computing workflows. The contextualization is similar to condor. There are three parameters:

    catalog_server=hostname or ip address
    workqueue_project=project name, defaults to "cernvm" (similar to the shared secret in condor)
    workqueue_user=user name, defaults to workqueue (the user is created on the fly if necessary)

In order to contextualize the master node, include an empty workqueue section, like

    [amiconfig]
    plugins=workqueue
    [workqueue]

In order to start the work queue workers, specify the location of the catalog server, like

    [amiconfig]
    plugins=workqueue

    [workqueue]
    catalog_server=128.142.142.107
    workqueue_project=foobar

The plugin will start one worker for every available CPU.

Once the ensemble is up and running, makeflow can make use of the workqueue resources like so

    makeflow -T wq -a -N foobar -d all -C 128.142.142.107:9097 makeflow.example

Note that your cloud infrastructure needs to provide access to UDP and TCP ports 9097 on your virtual machines.


## Known Issues

+ If the keyboard layout changes, run `sudo system-config-keyboard` to bring it back to match your keyboard


## Debugging

In case you cannot login (any more) to your virtual machine, even though the machine was properly contextualized, you can boot CernVM in "debug mode".  In the early boot menu, select the "Debug" entry.  This enables kernel debug messages and pauses the boot process just before the µCernVM bootloader hands over to the operating system.  Here, type `reset_root_password` followed by `ENTER` and `Ctrl+D`.  Once booted, you can then login as root with password "password".

If you experience hangs of the virtual machine after changing location, try to reset the network by `sudo /sbin/service network restart`.
