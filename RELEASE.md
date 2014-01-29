CernVM 3 First Public Release
=============================

## Overview

CernVM 3 is the out.
CernVM 3 is based on Scientific Linux 6 combined with a custom, virtualization-friendly Linux kernel.
It is also fully RPM based; you can use yum and rpm to install additional packages.

CernVM 3 is based on the µCernVM bootloader.
Its outstanding feature is that it does not require a hard disk image to be distributed (hence "micro").
Instead it is distributed as a read-only image of ~10MB containing a Linux kernel and the CernVM-FS client.
The rest of the operating system is downloaded and cached on demand by CernVM-FS.
The virtual machine still requires a hard disk as a persistent cache, but this hard disk is initially empty and can be created instantaneously, instead of being pre-created and distributed.

Since the operating system is loaded on demand from CernVM-FS, in constrast to CernVM 2 we can be more generous with respect to the packages that are preinstalled.
For instance, CernVM 3 comes with man pages, a C++11 compiler, a Go compiler, an Erlang interpreter, GNUplot, R, LaTeX, scipy and numpy, and many other useful packages.
For distributed computing, CernVM 3 comes with tools such as Condor, Ganglia, Squid, XrootD, CernVM CoPilot, Parrot and Workqueue/Makeflow, and others.
In order to manage your virtual machines in the cloud, CernVM 3 comes with the cloud management utilities for OpenStack (nova, glance), Amazon EC2 (ec2-... and euca-...), Google Compute Engine (gcutil), and Microsoft Azure (azure).

If you believe an important package is missing, please let us know!


## Installation

Download the latest images from [our download page](http://cernvm.cern.ch/portal/downloads).
In contrast to CernVM 2, there are no image flavors anymore.
There is only a single x86_64 image in different file formats.
This image can be contextualized to become either a graphical development VM or a batch virtual machine for the cloud.

Please also note that the CernVM Installer does not work with CernVM 3.
Eventually it is supposed to by replaced by the "Launch Now" button on the [CernVM Online](https://cernvm-online.cern.ch) website.
Currently this functionality is still fragile.


### Local Installation

For VMware, VirtualBox, Hyper-V and KVM Virtual Machine Manager on your laptop, download the CernVM ISO image.
Create a new virtual machine and attach the ISO image to it.
Additionally attach a new, empty hard drive of at least 20G.
Provide at least 1G of RAM to the virtual machine (your host needs at least 2G of RAM).

For KVM, ensure that the host provides "virtio" virtual hardware for block devices and network adapters.

For VirtualBox, ensure that you connect a second network adapter in "host only" mode.
In the settings, under "General" / "Advanced" enable bidirectional access for "Shared Clipboard" and "Drag'n'Drop".

CernVM 3 has VMware and VirtualBox guest additions included and selects them appropriately on boot.
There is no need to connect the guest addtions ISO image.
If you attach shared folders, they get mounted under /mnt/shared.

Once booted, use the context pairing mechanism from [CernVM Online](https://cernvm-online.cern.ch) to contextualize the VM.


### Cloud Installation

For IaaS clouds such as CERN openstack, Amazon EC2, or others use the "Filesystem" image for Xen based clouds and the "Raw" image for KVM based clouds.
For the "Filesystem" image, you need to attach additional ephemeral storage for the CernVM-FS cache.
For the "Raw" image, either attach ephemeral storage or ensure that the image is used as a root hard disk of 20G or more (default on CERN OpenStack).


### CERN OpenStack

On [CERN OpenStack](https://openstack.cern.ch), you need to upload the CernVM image to your project before you can create CernVM 3 instances.
To do so, download the CernVM 3 "Raw" image and download the openrc.sh file from the CERN OpenStack website.
Then run
    source openrc.sh
    export OS_CACERT=/etc/pki/tls/cert.pem
    glance image-create --name "CernVM 3.1.0" --is-public False --disk-format raw --property os=linux --property hypervisor_type=kvm --container-format bare --file ucernvm-prod.1.16-3.cernvm.x86_64.hdd
    nova boot "Virtual Machine Name" --image "CernVM 3.1.0" --flavor m1.small --key-name "name of the key pair"

If you don't need the image name registered with DNS, add `--meta cern-services=false` to the "nova boot" command in order to speed up instantiation.
Use at least m1.small as a flavor, the m1.tiny flavor is too small.


### Amazon EC2 Machine Images

A pre-built bundle on Amazon S3 is publicly available.
You can find it if you search for "CernVM" in the community provided AMIs.
In order to successfully boot CernVM on EC2, it requires ephemeral storage being attached to the EC2 instance.
You can use a CernVM 3 to manage your EC2 virtual machines; CernVM 3 already comes with the EC2 command line tools.

If you want to bundle and upload the image yourself, you can use the "Filesystem" format of the image.
The image needs to be bundled an [Amazon PV-GRUB](http://docs.aws.amazon.com/AWSEC2/2011-07-15/UserGuide/index.html?UserProvidedkernels.html) kernel (e.g. aki-825ea7eb)

## Updates

## Contextualization

### Next steps

Once booted and contextualized, you can use ssh to connect to your virtual machine.
SSHFS and shared folders provide you easy means to exchange files between the host and CernVM.

For storing data and analysis results, we recommend not to use the root partition.
Instead, attach a second hard drive to the virtual machine or use shared folders.
This way, you can move data between virtual machines and the data remains intact even in case the virtual machine ends up in an unsuable state.


## OpenAFS

CernVM has AFS installed but disabled by default.
In order to start AFS, you'd need to do
    sudo mkdir /afs
    sudo /sbin/chkconfig afs on
    sudo /sbin/service afs start

In our experience, AFS works poorly behind NAT.
So AFS might be helpful for CernVM on CERN OpenStack but it is not really an option for VMs on the laptop.
Instead, shared folders can provide an easy way to map directory trees from the host inside the guest.


## ROOT

In order to start a stand-alone ROOT, click on the tree logo in the middle of the application launcher bar.
In non-graphical mode, use `module load ROOT` to set the ROOT environemnt.
Afterwards you can just use `root`.
If you want to clean the environment from that particular version of ROOT, use `module unload ROOT`.


## C++11 Compiler

CernVM 3 comes with a C++11 compliant gcc 4.8 compiler installed side-by-side to the system compiler.
In order to enable it, run `source /opt/rh/devtoolset-2/enable`.
Apart from gcc 4.8, this also provides matching binutils and a matching gdb and Valgrind.


## Single Sign On

You can get a Kerberos token with `kinit`.
With the token, you can login to lxplus and work with subversion repositories without the need to provide a password.


## Known Issues

sudo system-config-keyboard Keyboard
Preload cache
Copy & Paste / DnD / Unity on VMware Fusion

## Debugging
