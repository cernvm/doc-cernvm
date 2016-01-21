# Running on CERN OpenStack

CernVM runs on CERN's private cloud [openstack.cern.ch](https://openstack.cern.ch/).  Like other OpenStack installations, the CERN cloud can be managed with [nova tools](http://information-technology.web.cern.ch/book/cern-private-cloud-user-guide/command-line-tools/openstack-tools). The nova tools are installed, for instance, on lxplus and on CernVM. The following steps can be used from a desktop CernVM.

If you haven't done so, you need to upload the CernVM image to your project before you can create CernVM 3 instances. To do so, download the CernVM 3 "Raw" image and download the openrc.sh file from the CERN OpenStack website. Then run

    source openrc.sh
    export OS_CACERT=/etc/pki/tls/cert.pem
    glance image-create --name "CernVM 3" --is-public False --disk-format raw --property os=linux \
      --property hypervisor_type=kvm --container-format bare \
      --file <cernvm-image>.hdd
    nova boot <Virtual Machine Image Name> --image "CernVM 3" --flavor m1.small \
      --key-name <OpenStack Keypair> --user-data <User Data File>

If you don't need the image name registered with DNS, add `--meta cern-services=false` to the "nova boot" command in order to speed up instantiation. For more sophisticated adjustments to CERN LanDB, please see the [CERN OpenStack documentation](http://information-technology.web.cern.ch/book/cern-private-cloud-user-guide/command-line-tools/openstack-tools#fastervm).

Use at least m1.small as a flavor, the m1.tiny flavor is too small. CERN also provides [optimized flavors for CernVM on OpenStack](https://information-technology.web.cern.ch/book/cern-cloud-infrastructure-user-guide/advanced-topics/flavors). Please contact the Cern OpenStack team in order to add them to your project.

For help on creating the user-data file, see our [contextualization page](http://cernvm.cern.ch/portal/contextualisation).
