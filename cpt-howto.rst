How to run on...
================

This section describes how to instantiate CernVM appliances on various local hypervisors and clouds.

VirtualBox
----------

CernVM Launch
~~~~~~~~~~~~~

The recommended way to start a CernVM with VirtualBox is using the :ref:`CernVM Launch <sct_launch>` utility.

Manual Instantiation
~~~~~~~~~~~~~~~~~~~~

To configure your VirtualBox for running CernVM do the following steps:

  * Start VirtualBox

    .. image:: _static/cvmvbox01.png

  * Click the "**New**" button and a "Create New Virtual Machine" dialogue will appear

    .. image:: _static/cvmvbox02.png

  * Enter the name of the virtual machine (e.g. "CernVM 4") and define the OS Type:

    * As the "**Type**" chose Linux
    * As the "**Version**" chose "Linux 2.6 / 3.x / 4.x (64 bit)"
    * Click "**Continue**"

      .. image:: _static/cvmvbox03.png

  * Define the amount of memory which you want to make available to the Virtual Machine (e.g. 2048 MB) and click ""**Continue**". Choose at least 1G of memory and leave at least 1G of memory free for your host.

    .. image:: _static/cvmvbox04.png

  * Configure the Virtual Machine hard drive.

    * Check the "**Create a virtual hard drive now**" option

    * As a hard drive file type, select "**VDI (VirtualBox Disk Image)**"

      .. image:: _static/cvmvbox05.png

    * For storage on physical hard drive, select "**Dynamically allocated**"

      .. image:: _static/cvmvbox06.png

    * Under file location and size, select the folder and file name of the virtual machine hard disk image and the maximum size. Select at least 20G for the size.

      .. image:: _static/cvmvbox07.png

  * Your new virtual machine will appear in the pane on the left.

    .. image:: _static/cvmvbox08.png

  * Click on "**Settings**"

    * Under "General", select the "Advanced" tab and choose "**Bidirectional**" for "Shared Clipboard" and "Drag and Drop"

      .. image:: _static/cvmvbox09.png

    * Under "Storage", click on the empty CD drive entry on the left. Then click on the little CD icon on the top right. Select the CernVM ISO image that you downloaded previously. The CernVM image should appear as CD entry in the left pane.

      .. image:: _static/cvmvbox11.png

    * Under "Network", click on the "**Adapter 2**" tab and enable the adapter as a "**Host-only Adapter**"

      .. image:: _static/cvmvbox12.png

    * Under "Graphics", select "**VBoxSVGA**" as a "Graphics Controller"

    * Close the settings dialog by clicking "**OK**".

Now you can Start the virtual machine by double clicking your virtual machine entry in the left pane. Once booted, you need to pair the virtual machine with a context defined in `CernVM Online <https://cernvm-online.cern.ch/>`_.

Shared Folders
~~~~~~~~~~~~~~

  * To configure created Virtual Machine, click on "**Settings**".

    .. image:: _static/cvmvbox08.png

  * Add the directories under "Shared Folders". Do *not* select the "Auto-mount" option. Inside the virtual machine, shared folders are automatically mounted under /mnt/shared.

    .. image:: _static/cvmvbox13.png

KVM
---

CernVM images for `KVM <https://www.linux-kvm.org/>`_ (Kernel-based Virtual Machine) are intended to be used by experienced users, or by system administrators. For creating and controlling virtual machines with KVM we recommend using libvirt (in particular ``virsh`` command line utility) and virt-manager graphical tool.

Prerequisies
~~~~~~~~~~~~

  * Make sure that your host supports kvm (the output of the command should not be empty)

    ::

      egrep '(vmx|svm)' --color=always /proc/cpuinfo

  * Make sure that you have kvm, bridge-utils, libvirt, and virt-manager packages installed. The output of the following commands should not be empty.

    ::

      lsmod | egrep 'kvm(_intel|_amd)'
      brctl --version
      virsh --version
      virt-manager --version # (only for graphical interface)

  * Make sure that the permissions of /dev/kvm file are set to 0660 (or more open). The file should be owned by “root”, and the group ownership should be set to “kvm”

    ::

      > ls -al /dev/kvm
      crw-rw---- 1 root kvm 10, 232 Oct 19 14:49 /dev/kvm

  * Make sure that KVM network is properly set up for using NAT

    ::

      > virsh net-dumpxml default
      <network>
        <name>default</name>
        <uuid>a6ae5d2a-8ab5-45a9-94b2-62c29eb9e4f4< /uuid>
        <forward mode='nat'/>
        <bridge name='virbr0' stp='on' forwardDelay='0' />
        <ip address='192.168.122.1' netmask='255.255.255.0'>
          <dhcp>
            <range start='192.168.122.2' end='192.168.122.254' />
          </dhcp>
        </ip>
      </network>


Creating a Virtual Machine
~~~~~~~~~~~~~~~~~~~~~~~~~~

Download CernVM ISO image from `CernVM Downloads page <http://cernvm.cern.ch/portal/downloads>`_. CernVM requires an empty hard drive as a persistent CernVM-FS cache. Create a sparse hard disk image file with dd:

::

  dd if=/dev/zero of=cernvm-hd.img bs=1 count=0 seek=20G

Create a virtual machine definition file for ``virsh`` (libvirt guest domain management interface), which should contain the following:

  * Virtual machine name
  * Memory size (in MB)
  * Number of virtual CPUs
  * Type of architecture ("x86_64") and boot device ("cdrom")
  * Hard drive and CD-ROM definition
  * Network interface definition
  * Graphical device definition

Example virtual machine definition file looks like this:

::

    <domain type='kvm'>
      <name>CernVM</name>
      <memory>2097152</memory>
      <vcpu>1</vcpu>
      <os>
        <type arch='x86_64'>hvm</type>
        <boot dev='cdrom' />
      </os>
      <features>
        <acpi />
        <apic />
        <pae />
      </features>
        <devices>
          <disk type='file' device='cdrom'>
            <source file='/data/test/cernvm4-micro-2020.04-1.iso' />
            <target dev="hdc" bus="ide" />
            <readonly />
          </disk>
          <disk type='file' device='disk'>
            <source file='/home/user/cernvm-hd.img' />
            <target dev='vda' bus="virtio" />
          </disk>
          <interface type='network'>
            <source network='default'/>
            <model type='virtio'/>
          </interface>

          <graphics type='vnc' listen='0.0.0.0' port='6019'/>
        </devices>
    </domain>

The virtual machine is created with the following command

::

    virsh create vm-definition.xml

Virtual machines can be listed, started, stopped, and removed with:

::

    > virsh list
     Id Name                 State
    ----------------------------------
     5  CernVM               running

    > virsh shutdown CernVM
    Domain CernVM is being shutdown

    > virsh start CernVM
    Domain CernVM started

    > virsh destroy CernVM
    Domain CernVM destroyed