.. _sct_context:

Contextualization
=================

Introduction
------------

A context is a small (up to 16kB), usually human-readable snippet that is used to apply a role to a virtual machine. A context allows to have a singe virtual machine image that can back many different virtual machine instances in so far as the instance can adapt to various cloud infrastructures and use cases depending on the context. In the process of contextualization, the cloud infrastructure makes the context available to the virtual machine and the virtual machine interprets the context. On contextualization, the virtual machine can, for instance, start certain services, create users, or set configuration parameters.

For contextualization, we distinguish between so called meta-data and user-data. The meta-data is provided by the cloud infrastructure and is not modifiable by the user. For example, meta-data includes the instance ID as issued by the cloud infrastructure and the virtual machine's assigned network parameters. The user-data is provided by the user on creation of the virtual machine.

Meta-data and user-data are typically accessible through an HTTP server on a private IP address such as 169.254.169.254. The cloud infrastructure shields user-data from different VMs so that it can be used to deliver credentials to a virtual machine.

In CernVM, there are three entities that interpret the user-data. Each of them typically reads "what it understands" while ignoring the rest. The µCernVM bootloader interprets a very limited set of key-value pairs that are used to initialize the virtual hardware and to select the CernVM-FS operating system repository. In a later boot phase, amiconfig and cloud-init are used to contextualize the virtual machine. The amiconfig system was initially provided by rPath but it is now maintained by us. It provides very simple, key-value based contextualization that is processed by a number of amiconfig plugins. The cloud-init system is maintained by Redhat and Ubuntu and provides a more sophisticated but also slightly more complex contextualization mechanism.


Contextualization of the µCernVM Boot Loader
--------------------------------------------

The µCernVM bootloader can process EC2, Openstack, and vSphere user data. Within the user data everything is ignored expect a block of the form

::

    [ucernvm-begin]
    key1=value1
    key2=value2
    ...
    [ucernvm-end]


The following key-value pairs are recognized:

  * **resize_rootfs**: Can be **on** or **off**. When turned on, use all of the hard disk as root partition instead of the first 20G
  * **cvmfs_http_proxy**: HTTP proxy in CernVM-FS notation
  * **cvmfs_pac_urls**: WPAD proxy autoconfig URLs separated by ';'
  * **cvmfs_server**: List of Stratum 1 servers, e.g. cvmfs-stratum-one.cern.ch,another.com
  * **cvmfs_tag**: The snapshot name, useful for the long-term data preservation
  * **cernvm_inject**: Base64 encoded .tar.gz ball, which gets extracted in the root tree
  * **useglideinWMS**: Can be **on** or **off**, defaults to on. When turned off, :ref:`glideinWMS <sct_glideinwms>` auto detection gets disabled


Contextualization with amiconfig
--------------------------------

The amiconfig contextualization executes on boot time, parses user data and looks for python style configuration blocks. If a match is found the corresponding plugin will process the options and execute configuration steps if needed. By default, enabled rootsshkeys is the only enabled plugins (others can be enabled in the configuration file).

Default plugins:

::

    rootshkeys            - allow injection of root ssh keys

Available plugins

::

    cernvm                - configure various CernVM options
    condor                - setup Condor batch system
    disablesshpasswdauth  - if activated, it will disable ssh authentication with password
    dnsupdate             - update DNS server with current host IO
    ganglia               - configure gmond (ganglia monitoring)
    hostname              - set hostname
    noip                  - register IP address with NOIP dynamic DNS service
    nss                   - /etc/nsswithch.conf configuration
    puppet                - set parameters for puppet configuration management
    squid                 - configure squid for use with CernVM-FS

Common amiconfig options:

::

    [amiconfig]
    plugins = <list of plugins to enable>
    disabed_plugins = <list of plugins to disable>

Specific plugin options:

::

    [cernvm]
    # list of ',' seperated organisations/experiments (lowercase)
    organisations = <list>
    # list of ',' seperated repositories (lowercase)
    repositories = <list>
    # list of ',' separated user accounts to create <user:group:[password]>
    users = <list>
    # CernVM user shell </bin/bash|/bin/tcsh>
    shell = <shell>
    # CVMFS HTTP proxy
    proxy = http://<host>:<port>;DIRECT
    ----------------------------------------------------------
    # url from where to retrieve initial CernVM configuration
    config_url = <url>
    # list of ',' separated scripts to be executed as given user: <user>:/path/to/script.sh
    contextualization_command = <list>
    # list of ',' seperated services to start
    services = <list>
    # extra environment variables to define
    environment = VAR1=<value>,VAR2=<value>

::

    [condor]
    # host name
    hostname = <FQDN>
    # master host name
    condor_master = <FQDN>
    # shared secret key
    condor_secret = <string>
    #------------------------
    # collector name
    collector_name = <string>
    # condor user
    condor_user = <string>
    # condor group
    condor_group = <string>
    # condor directory
    condor_dir = <path>
    # condor admin
    condor_admin = <path>
    highport = 9700
    lowport = 9600
    uid_domain =  filesystem_domain =  allow_write = *.$uid_domain extra_vars = use_ips =


Contextualization scripts
~~~~~~~~~~~~~~~~~~~~~~~~~

If the user data string starts with a line starting with ``#!``, it will be interpreted as a bash script and executed. The same user data string may as well contain amiconfig contextualization options but they must be placed after the configuration script which must end with an exit statement. The interpreter can be ``/bin/sh`` or ``/bin/sh.before`` or ``/bin/sh.after`` depending on when the script is to be executed, before or after amiconfig contextualization. A script for the ``/bin/sh`` interpreter is executed after amiconfig contextualization.


Contextualization with cloud-init
---------------------------------

As an alternative to amiconfig, CernVM supports `cloud-init contextualization <https://cloudinit.readthedocs.org/en/latest/index.html>`_.


Mixing user-data for µCernVM, amiconfig, and cloud-init
-------------------------------------------------------

The user-data for cloud-init and for amiconfig can be mixed. The cloud-init syntax supports user data divided into multiple `MIME <https://en.wikipedia.org/wiki/MIME>`_ parts. One of these MIME parts can contain amiconfig or µCernVM formatted user-data. All contextualization agents (µCernVM, amiconfig, cloud-init) parse the user data and each one interprets what it understands.

The following example illustrates how to mix amiconfig and cloud-init. We have an amiconfig context amiconfig-user-data that starts a catalog server for use with Makeflow:

::

    [amiconfig]
    plugins = workqueue
    [workqueue]

We also have a cloud-init context cloud-init-user-data that creates an interactive user "cloudy" with the password "password"

::

    users:
      - name: cloudy
        lock-passwd: false
        passwd: $6$XYWYJCb.$OYPPN5AohCixcG3IqcmXK7.yJ/wr.TwEu23gaVqZZpfdgtFo8X/Z3u0NbBkXa4tuwu3OhCxBD/XtcSUbcvXBn1

The following helper script creates our combined user data with multiple MIME parts:

::

    amiconfig-mime cloud-init-user-data:cloud-config amiconfig-user-data:amiconfig-user-data > mixed-user-data

In the same way, the µCernVM contextualization block can be another MIME part in a mixed context with MIME type ucernvm.


.. _sct_glideinwms:

glideinWMS User Data
--------------------

By default, CernVM will automatically detect user data from glideinWMS and, if detected, activate the glideinWMS VM agent. CernVM recognizes user data that consists of no more than two lines and that contains the pattern ``...#### -cluster 0123 -subcluster 4567####...`` as glideinWMS user data. It will automatically extract the CernVM-FS proxy configuration (proxy and pac URLs) from the user data. In order to disable autodetection, set ``useglideinWMS=false`` in the µCernVM contextualization.


Extra Contextualization
-----------------------

In addition to the normal user data, we have experimental support for "`extra user data <https://github.com/cernvm/cernvm-micro#extra-user-data>`_", which might be a last resort where the normal user data is occupied by the infrastructure. For instance, glideinWMS seems to exclusively specify user data, making it necessary to modify the image for additional contextualization. Extra user data are injected in the image under /cernvm/extra-user-data and they are internally appended to the normal user data. This does not yet work with cloud-init though; only with amiconfig and the µCernVM bootloader.


Applying User Data
------------------

CernVM supports applying contextualization information at boot time using one of the following mechanisms:

  * User-Data text snippet: almost all of the private or public cloud infrastructures provide a mechanism of passing arbitrary data to the instance at the creation time. A good example is `Amazon's Instance Metadata for EC2 <https://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/AESDG-chapter-instancedata.html>`_.

  * CD-ROM: the user data are stored to CD-ROM ISO images that are attached to the virtual machine.

Both mechanisms eventually pass a string of ini-like data to the instance.


Preparing a User-Data CD-ROM Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If it is not possible pass the user-data by the cloud infrastructure, you can use the mechanism of a contextualization CD-ROM image. This image must contain at least one file called ``context.sh`` and this file must have at least the following two lines:

::

    EC2_USER_DATA="<user-data>"
    ONE_CONTEXT_PATH="/var/lib/amiconfig"

Where ``<user-data>`` is the base64-encoded user data text snippet created as decribed earlier.

To create the CD-ROM image (for example user-data.iso) you can then use the ``mkisofs`` utility:

::

    mkdir iso-tmp
    echo 'EC2_USER_DATA=123abc...' >> iso-tmp/context.sh
    echo 'ONE_CONTEXT_PATH="/var/lib/amiconfig"' >> iso-tmp/context.sh
    mkisofs -o user-data.iso iso-tmp

You must then mount this CD-ROM image to you virtual machine before you boot it. This is done differently on every hypervisor, so check your hypervisor configuration for more information.
