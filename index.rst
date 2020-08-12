.. CernVM Virtual Machine documentation master file

Welcome to CernVM Virtual Machine documentation!
================================================

What is the CernVM Virtual Machine?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CernVM is a virtual machine image based on CentOS combined with a custom,
virtualization-friendly Linux kernel.

CernVM is based on the `µCernVM bootloader <https://arxiv.org/abs/1311.2426>`_.
Its outstanding feature is that it does not require a hard disk image to be
distributed (hence "micro"). Instead it is distributed as a read-only image of
~20MB containing a Linux kernel and the CernVM-FS client. The rest of the
operating system is downloaded and cached on demand by CernVM-FS. The virtual
machine still requires a hard disk as a persistent cache, but this hard disk is
initially empty and can be created instantaneously.

Contents
^^^^^^^^

.. toctree::
   :maxdepth: 2

   cpt-releasenotes
   cpt-launch
   cpt-context
   cpt-bootloader
   cpt-signatures


Contact and Authors
^^^^^^^^^^^^^^^^^^^

Visit our website on `cernvm.cern.ch <http://cernvm.cern.ch/>`_.

Authors of this documentation:

   * Jakob Blomer
