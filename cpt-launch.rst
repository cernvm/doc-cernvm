CernVM Launch
=============

**Note**: CernVM Launch does currently not work with VirtualBox 6.1. We are working on a fix. Please use VirtualBox 6.0 for the time being.

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
