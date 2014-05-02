CernVM 3 First Public Release
=============================

## Overview

CernVM 3 is out. CernVM 3 is based on Scientific Linux 6 combined with a custom, virtualization-friendly Linux kernel. It is also fully RPM based; you can use yum and rpm to install additional packages.

CernVM 3 is based on the [µCernVM bootloader](http://arxiv.org/abs/1311.2426).  Its outstanding feature is that it does not require a hard disk image to be distributed (hence "micro").  Instead it is distributed as a read-only image of ~10MB containing a Linux kernel and the CernVM-FS client.  The rest of the operating system is downloaded and cached on demand by CernVM-FS.  The virtual machine still requires a hard disk as a persistent cache, but this hard disk is initially empty and can be created instantaneously, instead of being pre-created and distributed.

Since the operating system is loaded on demand from CernVM-FS, in constrast to CernVM 2 we can be more generous with respect to the packages that are preinstalled.  For instance, CernVM 3 comes with man pages, a C++11 compiler, a Go compiler, an Erlang interpreter, GNUplot, R, LaTeX, scipy and numpy, and many other useful packages.  For distributed computing, CernVM 3 comes with tools such as Condor, Ganglia, Squid, XrootD, Puppet, CernVM CoPilot, Parrot and Workqueue/Makeflow, and others.  In order to manage your virtual machines in the cloud, CernVM 3 comes with the cloud management utilities for OpenStack (nova, glance), Amazon EC2 (ec2-... and euca-...), Google Compute Engine (gcutil), and Microsoft Azure (azure).

If you believe an important package is missing, please let us know!


## Installation

Download the latest images from [our download page](http://cernvm.cern.ch/portal/downloads).  In contrast to CernVM 2, there are no image flavors anymore.  There is only a single x86_64 image in different file formats.  This image can be contextualized to become either a graphical development VM or a batch virtual machine for the cloud.

Please also note that the CernVM Installer does not work with CernVM 3.  Eventually it is supposed to by replaced by the "Launch Now" button on the [CernVM Online](https://cernvm-online.cern.ch) website.  Currently this functionality is still fragile.


### Local Installation

For VMware, VirtualBox, Hyper-V and KVM Virtual Machine Manager on your laptop, download the CernVM ISO image.  Create a new virtual machine and attach the ISO image to it.  Additionally attach a new, empty hard drive of at least 20G.  Provide at least 1G of RAM to the virtual machine (your host needs at least 2G of RAM).

For KVM, ensure that the host provides "virtio" virtual hardware for block devices and network adapters.

For VirtualBox, ensure that you connect a second network adapter in "host only" mode.  In the settings, under "General" / "Advanced" enable bidirectional access for "Shared Clipboard" and "Drag'n'Drop".

CernVM 3 has VMware and VirtualBox guest additions included and selects them appropriately on boot.  There is no need to connect the guest addtions ISO image.  If you attach shared folders, they get mounted under /mnt/shared.

Once booted, use the context pairing mechanism from [CernVM Online](https://cernvm-online.cern.ch) to contextualize the VM.


### Cloud Installation

For IaaS clouds such as CERN openstack, Amazon EC2, or others use the "Filesystem" image for Xen based clouds and the "Raw" image for KVM based clouds.  For the "Filesystem" image, you need to attach additional ephemeral storage for the CernVM-FS cache.  For the "Raw" image, either attach ephemeral storage or ensure that the image is used as a root hard disk of 20G or more (default on CERN OpenStack).


### CERN OpenStack

On [CERN OpenStack](https://openstack.cern.ch), you need to upload the CernVM image to your project before you can create CernVM 3 instances.  To do so, download the CernVM 3 "Raw" image and download the openrc.sh file from the CERN OpenStack website.
Then run

    source openrc.sh
    export OS_CACERT=/etc/pki/tls/cert.pem
    glance image-create --name "CernVM 3" --is-public False --disk-format raw --property os=linux \
      --property hypervisor_type=kvm --container-format bare \
      --file ucernvm-prod.1.16-3.cernvm.x86_64.hdd
    nova boot "Virtual Machine Name" --image "CernVM 3" --flavor m1.small --key-name "name of the key pair" \
      --user-data $user-data-file

If you don't need the image name registered with DNS, add `--meta cern-services=false` to the "nova boot" command in order to speed up instantiation.  Use at least m1.small as a flavor, the m1.tiny flavor is too small.


### Amazon EC2 Machine Images

A pre-built bundle on Amazon S3 is publicly available.  You can find it if you search for "CernVM" in the community provided AMIs.  In order to successfully boot CernVM on EC2, it requires ephemeral storage being attached to the EC2 instance.  You can use a CernVM 3 to manage your EC2 virtual machines; CernVM 3 already comes with the EC2 command line tools.  To instantiate an EC2 machine from a CernVM 3 on your laptop, you can use for instance

    ec2-run-instances $ami_id -b /dev/sdc=ephemeral0 -n 1 -k $keyname -t m1.small -f $user-data -g default

If you want to bundle and upload the image yourself, you can use the "Filesystem" format of the image.  The image needs to be bundled an [Amazon PV-GRUB](http://docs.aws.amazon.com/AWSEC2/2011-07-15/UserGuide/index.html?UserProvidedkernels.html) kernel (e.g. aki-825ea7eb)


## Contextualization

A CernVM 3 needs to be contextualized on first boot.  The process of contextualization assigns a profile to the particular CernVM 3 instance.  For instance, a CernVM can have the profile of a graphical VM used for development on a laptop; applying another context let the CernVM become a worker node in the cloud.

The [CernVM Online portal](https://cernvm-online.cern.ch) lets you define and store VM profiles in one place.
Once defined, the VM profiles can quickly be applied to any newly booted CernVM instance using a pairing mechanism on the login prompt.  Please visit the following pages for more information about how to [create new context templates](http://cernvm.cern.ch/portal/online/documentation/create-new-context) and [pair an instance](http://cernvm.cern.ch/portal/online/documentation/pairing-the-instance) with given template.

Also check out the [CernVM Online Marketplace](https://cernvm-online.cern.ch/market/list).  We will keep adding ready-to-use contexts for the most common use cases.

### Cloud Contextualization

Like CernVM 2, CernVM 3 supports the [amiconfig and CD-ROM contextualization methods](http://cernvm.cern.ch/portal/contextualisation).  In addition, CernVM 3 supports [cloud-init contextualization](https://cloudinit.readthedocs.org/en/latest/index.html).

#### Condor, Ganglia, and CernVM-FS

Some of the contextualization tasks done by amiconfig can be done by cloud-init as well due to the native cloud-init modules for [cvmfs, ganglia, and condor](https://twiki.cern.ch/twiki/bin/view/LCG/CloudInit).  These modules are part of CernVM 3.


#### Mixing cloud-init and amiconfig user data

The user-data for cloud-init and for amiconfig can be mixed.  The cloud-init syntax supports user data divided into multiple MIME parts.  One of these MIME parts can contain amiconfig formatted user-data.  Both contextualization agents (cloud-init and amiconfig) parse the user data and each one interprets what it understands.

The following example illustrates how to mix amiconfig and cloud-init.  We have an amiconfig context `amiconfig-user-data` that starts a catalog server for use with Makeflow:

    [amiconfig]
    plugins = workqueue
    [workqueue]

We also have a cloud-init context `cloud-init-user-data` that creates an interactive user "cloudy" with the password "password"

    users:
      - name: cloudy
        lock-passwd: false
        passwd: $6$XYWYJCb.$OYPPN5AohCixcG3IqcmXK7.yJ/wr.TwEu23gaVqZZpfdgtFo8X/Z3u0NbBkXa4tuwu3OhCxBD/XtcSUbcvXBn1

The following helper script creates our combined user data with multiple MIME parts:

    #!/usr/bin/python
    import sys
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    if len(sys.argv) == 1:
        print("%s input-file:type ..." % (sys.argv[0]))
        sys.exit(1)

    combined_message = MIMEMultipart()
        for i in sys.argv[1:]:
            (filename, format_type) = i.split(":", 1)
        with open(filename) as fh:
            contents = fh.read()
        sub_message = MIMEText(contents, format_type, sys.getdefaultencoding())
        sub_message.add_header('Content-Disposition', 'attachment; filename="%s"' % (filename))
        combined_message.attach(sub_message)

    print(combined_message)

We invoke it like

    python helper.py cloud-init-user-data:cloud-config amiconfig-user-data:amiconfig > mixed-user-data


#### Contextualizing the µCernVM Bootloader

The µCernVM bootloader can process EC2, Openstack, and vSphere user data.  Within the user data everything is ignored expect a block of the form

    [ucernvm-begin]
    key1=value1
    key2=value2
    ...
    [ucernvm-end]

In the same way as mixing amiconfig and cloud-init user data, this block can also be a MIME part in a mixed context.
The following key-value pairs are recognized:

| Key             | Value                             | Comments                                         |
|-----------------|-----------------------------------|--------------------------------------------------|
|resize_rootfs    | on/off                            | use all of the harddisk instead of the first 20G |
|cvmfs_http_proxy | HTTP proxy in CernVM-FS notation  |                                                  |
|cvmfs_server     | List of Stratum 1 servers         | E.g.: cvmfs-stratum-one.cern.ch,another.com      |
|cvmfs_tag        | The snapshot name                 | For long-term data preservation                  |


#### Extra Contextualization

In addition to the normal user data, we have experimental support for "[extra user data](https://github.com/cernvm/cernvm-micro#extra-user-data)", which might be a last resort where the normal user data is occupied by the infrastructure.  For instance, glideinWMS seems to exclusively specify user data, making it necessary to modify the image for additional contextualization.  Extra user data are injected in the image under /cernvm/extra-user-data and they are internally appended to the normal user data.  This does not yet work with cloud-init though; only with amiconfig and the µCernVM bootloader.


## Updates

When booted, CernVM will load the latest available CernVM 3 version and pin itself on this version.  This ensures that your environment stays the same unless you explicitly take action.  Both the µCernVM bootloader and the CernVM-FS provided operating system can be updated using the `cernvm-update` script.  The support list will be notified when updates are ready and will post specific instructions for each update.

Note that due to the different nature of CernVM 2 and CernVM 3 there is no upgrade path from CernVM 2 to CernVM 3.

The CernVM 3 strong version number consists of 4 parts: 3.X.Y.Z.  Major version 3 indicates an Scientific Linux 6 based CernVM.  Minor version X will be changed when there is a significant change in the set of supported features.  "Y" is the bugfix version.  "Z" is the security hotfix version; changes in "Z" don't change the set of packages but provide security fixes for selected packages.


## Next steps

Once booted and contextualized, you can use ssh to connect to your virtual machine.  [SSHFS](http://fuse.sourceforge.net/sshfs.html) and shared folders provide you an easy means to exchange files between the host and CernVM.

For storing data and analysis results, we recommend not to use the root partition.  Instead, attach a second hard drive to the virtual machine or use shared folders.  This way, you can move data between virtual machines and the data remains intact even in case the virtual machine ends up in an unsuable state.


## OpenAFS

CernVM has AFS installed but disabled by default.  In order to start AFS, you'd need to do

    sudo mkdir /afs
    sudo /sbin/chkconfig afs on
    sudo /sbin/service afs start

Once mounted, you can get an AFS token using `kinit` followed by `aklog`.  In our experience, AFS works poorly behind NAT.  So AFS might be helpful for CernVM on CERN OpenStack but it is not really an option for VMs on the laptop.  Instead, shared folders can provide an easy way to map directory trees from the host inside the guest.


## ROOT

In order to start a stand-alone ROOT, click on the tree logo in the middle of the application launcher bar.  In non-graphical mode, use `module load ROOT` to set up the ROOT environemnt.  Afterwards you can just use `root`.  If you want to clean the environment from that particular version of ROOT, use `module unload ROOT`.


## C++11 Compiler

CernVM 3 comes with a C++11 compliant gcc 4.8 compiler that can be used in lieu of the Scientific Linux 6 system compiler.  In order to enable it, run `source /opt/rh/devtoolset-2/enable`.  Apart from gcc 4.8, this also provides matching binutils and a matching gdb and Valgrind.


## Makeflow

CernVM 3 supports the [Makeflow](http://www.cse.nd.edu/~ccl/software/makeflow/) workflow engine.  Makeflow provides an easy way to define and run distributed computing workflows.  The contextualization is similar to condor.  There are three parameters:

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


## Single Sign On

You can get a Kerberos token with `kinit`.  With the token, you can login to lxplus and work with subversion repositories without the need to provide a password.


## Known Issues

+ If the keyboard layout changes, run `sudo system-config-keyboard` to bring it back to match your keyboard
+ Copy & Paste, Drag and Drop, and Unity features do not work on VMware Fusion


## Debugging

In case you cannot login (any more) to your virtual machine, even though the machine was properly contextualized, you can boot CernVM in "debug mode".  In the early boot menu, select the "Debug" entry.  This enables kernel debug messages and pauses the boot process just before the µCernVM bootloader hands over to the operating system.  Here, type `reset_root_password` followed by `ENTER` and `Ctrl+D`.  Once booted, you can then login as root with password "password".

If you experience hangs of the virtual machine after changing location, try to reset the network by `sudo /sbin/service network restart`.
