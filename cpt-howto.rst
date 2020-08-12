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
