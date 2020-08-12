.. _sct_release:

Release Notes
=============

CernVM 4.4 [17.06.2020]
-----------------------

CernVM 4.4 is a minor update to CernVM 4. It upgrades the base system to EL 7.8 and it updates the certificate chain to fix contextualization with CernVM Online.

**Note**: if your bootloader is older than version 2020.04-1, you need to run

::

    sudo cp /etc/cvmfs/keys/cern.ch/cern-it4.cern.ch.pub /mnt/.rw/aux/keys/cernvm-prod.cern.ch
    sudo cernvm-update -k

before being able to update with ``sudo cernvm-update -a``.


CernVM 4.3 [27.01.2020]
-----------------------

CernVM 4.3 is a minor update to CernVM 4.2. It upgrades the base system to
EL 7.7 and provides new versions of the docker and eos packages. Note that in
the course of the EOS update, that eosd daemon disappeared. Instead, eos mounts
are now autofs managed, in the same way they are on CERN lxplus.


CernVM 4.2 [04.02.2019]
-----------------------

CernVM 4.2 is a minor update to CernVM 4.1, upgrading the base system to EL 7.6.


CernVM 4.1 [12.06.2018]
-----------------------

Installation
~~~~~~~~~~~~

Download the latest images from our `download page <https://cernvm.cern.ch/portal/downloads>`_. The image is generic and available in different file formats for different hypervisors. The image needs to be contextualized to become either a graphical development VM or a batch virtual machine for the cloud.

Detailed instructions are available for :ref:`VirtualBox <sct_vbox>`, :ref:`KVM <sct_kvm>`, :ref:`Docker <sct_docker>`, :ref:`OpenStack <sct_openstack>`, :ref:`Amazon EC2 <sct_ec2>`, :ref:`Google Compute Engine <sct_gce>`, and :ref:`Microsoft Azure <sct_azure>`.


Contextualization
~~~~~~~~~~~~~~~~~

In most cases, a CernVM needs to be contextualized on first boot. The process of contextualization assigns a profile to the particular CernVM instance. For instance, a CernVM can have the profile of a graphical VM used for development on a laptop; applying another context let the CernVM become a worker node in the cloud.

The :ref:`CernVM Launcher <sct_launch>` allows for instantiating CernVMs from text-based contexts, such as our `public demo contexts <https://github.com/cernvm/public-contexts>`_.

Please find details on the various contextualiztion options on the :ref:`contextualization page <sct_context>`.


Updates and Version Numbers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When booted, CernVM will load the latest available CernVM version and pin itself on this version. This ensures that your environment stays the same unless you explicitly take action. Both the µCernVM bootloader and the CernVM-FS provided operating system can be updated using the ``cernvm-update`` script. CernVM machines show an update notification in /etc/motd and in the GUI. The support list will be notified when updates are ready and will post specific instructions for each update.

The CernVM 4 strong version number consists of 4 parts: 4.X.Y.Z. Major version 4 indicates an Scientific Linux 7 based CernVM. Minor version X will be changed when there is a significant change in the set of supported features. “Y” is the bugfix version. “Z” is the security hotfix version; changes in “Z” don’t change the set of packages but provide security fixes for selected packages.

Next Steps
~~~~~~~~~~

Once booted and contextualized, you can use ssh to connect to your virtual machine. `SSHFS <https://github.com/libfuse/sshfs>`_ and shared folders provide you an easy means to exchange files between the host and CernVM.

For storing data and analysis results, we recommend not to use the root partition. Instead, attach a second hard drive to the virtual machine or use shared folders. This way, you can move data between virtual machines and the data remains intact even in case the virtual machine ends up in an unsuable state.


Single Sign On
~~~~~~~~~~~~~~

You can get a Kerberos token with ``kinit``. With the token, you can login to lxplus and work with subversion repositories without the need to provide a password.


Swap Space
~~~~~~~~~~

By default, CernVM has no swap space enabled. The following commands creates a 2G swap file

::

    sudo fallocate -l 2G /mnt/.rw/swapfile
    sudo chmod 0600 /mnt/.rw/swapfile
    sudo mkswap /mnt/.rw/swapfile
    sudo swapon /mnt/.rw/swapfile

If a file /mnt/.rw/swapfile exists, it will picked up automatically on boot as a swap space. In order to activate a swap space through contextualization, add to your amiconfig user data

::

    [cernvm]
    swap_size=<SIZE>

where ``<SIZE>`` can be anything understood by ``fallocate -l`` or it can be ``auto``, in which case CernVM uses 2G/core.


Resizing the Root Partition
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you increase your virtual hard drive, you can have CernVM increase your root partition accordingly. To do so, run

::

    sudo touch /mnt/.rw/aux/resize

and reboot. Resizing the root partition is a delicate operation, please **make a VM snapshot before you proceed**.


Debugging
~~~~~~~~~

In case you cannot login (any more) to your virtual machine, even though the machine was properly contextualized, you can boot CernVM in "debug mode". In the early boot menu, select the "Debug" entry. This enables kernel debug messages and pauses the boot process just before the µCernVM bootloader hands over to the operating system. Here, type ``reset_root_password`` followed by ``ENTER`` and ``Ctrl+D``. Once booted, you can then login as root with password "password".
