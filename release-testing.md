# Checklist Hypervisors
+ Start and contextualize as OVA in VBox
+ Start in KVM, test reaction to power button
+ Start in VMware
+ Use CernVM to start in CERN OpenStack

    source openrc.sh
    export OS_CACERT=/etc/pki/tls/cert.pem
    wget http://cernvm.cern.ch/releases/ucernvm-images.1.17-10.cernvm.x86_64/ucernvm-testing.1.17-10.cernvm.x86_64.hdd
    glance image-create --name cernvm-3.2 --is-public False --disk-format raw --property os=linux --property hypervisor_type=kvm --container-format bare --file ucernvm-testing.1.17-10.cernvm.x86_64.hdd
    nova boot cvm-test-36 --image cernvm-3.2 --flavor m1.medium --key-name cernvm-openstack --user-data user-data-mixed --meta cern-services=false

+ Use CernVM to start on EC2
    wget http://cernvm.cern.ch/releases/ucernvm-images.1.17-10.cernvm.x86_64/ucernvm-testing.1.17-10.cernvm.x86_64.fat
    mkdir bundle
    ec2-bundle-image -c cert.pem -k pk.pem -u AWSACCOUNTID -i ucernvm-testing.1.17-10.cernvm.x86_64.fat --debug --destination bundle --arch x86_64 --kernel aki-919dcaf8
    ec2-upload-bundle -m bundle/ucernvm-testing.1.17-10.cernvm.x86_64.fat.manifest.xml -b cernvm3 -a ACCESSKEY -s SECRETKEY
    ec2-register -O ACCESSKEY -W SECRETKET -a x86_64 cernvm3/ucernvm-testing.1.17-10.cernvm.x86_64.fat.manifest.xml  -d "CernVM 3.2 Testing"
    ec2-run-instances ami-7a55b312 -n 1 -k cvm-test-key -t m3.medium -f user-data -g default
    (careful, small disk.  Don't add swap)

    Login as repomgr, root

+ Use CernVM to start on GCE
    wget http://cernvm.cern.ch/releases/ucernvm-images.1.17-10.cernvm.x86_64/ucernvm-testing.1.17-10.cernvm.x86_64.tar.gz
    gsutil cp ucernvm-testing.1.17-10.cernvm.x86_64.tar.gz gs://cvm3/ucernvm-testing.1.17-10.cernvm.x86_64.tar.gz
    gcutil addimage cernvm3 gs://cvm3/ucernvm-testing.1.17-10.cernvm.x86_64.tar.gz --project cernvm-test
    ssh-keygen -f cvm-keypair
    gcutil addinstance --image=cernvm3 --kernel="" <INSTANCE NAME> --metadata=cvm-user-data:$(base64 -w0 user-data) --authorized_ssh_keys=root:cvm-keypair.pub --project cernvm-test

+ Use CernVM to start on Azure

    wget http://cernvm.cern.ch/releases/ucernvm-images.2.2-0.cernvm.x86_64/ucernvm-devel.2.2-0.cernvm.x86_64.vhd
    azure account download
    azure account import <CREDENTIALS FILE>
    azure storage account set cernvm01
    azure storage account connectionstring show cernvm01
    export AZURE_STORAGE_CONNECTION_STRING="<CONNECTION STRING>"
    export AZURE_STORAGE_ACCESS_KEY="<ACCESS KEY>"
    azure vm disk upload ucernvm-devel.2.2-0.cernvm.x86_64.vhd https://cernvm01.blob.core.windows.net/images/ucernvm-devel.2.2-0.cernvm.x86_64.vhd $AZURE_STORAGE_ACCESS_KEY
    azure vm image create --os linux --blob-url https://cernvm01.blob.core.windows.net/images/ucernvm-devel.2.2-0.cernvm.x86_64.vhd cvm35-test01
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout cvm-azure.key -out cvm-azure.pem
    chmod 0600 cvm-azure.key
    azure vm create i-cvm35-test01 cvm35-test01 --ssh --ssh-cert cvm-azure.pem --custom-data user-data-mixed --location "West Europe" azure "@Aa0$(cat /dev/urandom | tr -cd [:alnum:] | head -c24)"
    azure vm show i-cvm35-test01

User data:

    [cernvm]
    organisations=None
    repositories=
    shell=/bin/bash
    config_url=http://cernvm.cern.ch/config
    users=repomgr:repomgr:Taschentuch
    edition=Batch
    swap_size=auto  # careful, on GCE there might not be enough disk space

Cloud-init user data:

    users:
      - name: cloudy
        lock-passwd: false
        passwd: $6$XYWYJCb.$OYPPN5AohCixcG3IqcmXK7.yJ/wr.TwEu23gaVqZZpfdgtFo8X/Z3u0NbBkXa4tuwu3OhCxBD/XtcSUbcvXBn1

Combine: `amiconfig-mime user-data-cloudinit:cloud-config user-data:amiconfig-user-data > user-data-mixed`

# Start vagrant boxes on Windows, Linux, Mac

    vagrant box add --force --name cvm-test <box>
    vagrant init cvm-test
    vagrant up
    vagrant ssh

# Checklist CERN OpenStack
+ Check for sane /root/.ssh/authorized_keys
+ Check for afs
+ Check for cloud-init / amiconfig mixed user data

# Checklist VBox, VMware
+ Shutdown from GUI as normal user
+ No error messages at boot
+ No error messages during after-init-reboot
+ Suspend and resume
+ Check for correct time / running ntpd
+ Login via ssh
+ Start ROOT
+ Start glxgears
+ Check /dev/shm
+ Check mouse integration
+ Check resizing window
+ Check Unity
+ Check copy & paste
+ Check shared folders


# VMware or VirtualBox
+ no surprising cron jobs in /etc/cron.daily / cron.hourly / cron.d
+ root should not be able to login
+ open a screen (as root and as normal user)
+ Start a Docker container
    sudo service docker start
    docker run -i ubuntu /bin/bash
+ Create contextualized OVA image with cvm2ova
+ Test xrdp service
+ Start httpd
+ contexutalize with a password protected context
+ ls /cvmfs/atlas.cern.ch /cvmfs/atlas-condb.cern.ch /cvmfs/atlas-nightlies.cern.ch /cvmfs/sft.cern.ch /cvmfs/grid.cern.ch
+ Pull the network cable and reboot, can take longer but should not hang
+ SSO (ssh) through Kerberos (kinit)  [work on VMware only]
+ Access oasis.opensciencegrid.org, ilc.desy.de, wenmr.egi.eu
+ ATLAS event display

    source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
    asetup 19.0.0
    vp1

+ LHCb event display

    source /cvmfs/lhcb.cern.ch/etc/login.sh
    SetupProject Panoramix
    python $myPanoramix -f none

    # Alternatively

    source /cvmfs/lhcb.cern.ch/lib/lhcb/LBSCRIPTS/prod/InstallArea/scripts/LbLogin.sh -c x86_64-slc6-gcc48-opt
    SetupProject Panoramix v23r0
    python $myPanoramix -f none

+ ALICE event display

    . /cvmfs/alice.cern.ch/etc/login.sh
    alienv enter AliRoot/v5-05-Rev-32-1
    alieve

+ CMS event display

    . /cvmfs/cms.cern.ch/cmsset_default.sh
    cmsrel CMSSW_7_0_0
    cd CMSSW_7_0_0
    cmsenv
    cmsShow

+ LHCb test job

    source /cvmfs/lhcb.cern.ch/etc/login.sh
    SetupProject Brunel v50r1 --use PRConfig
    gaudirun.py /cvmfs/lhcb.cern.ch/lib/lhcb/DBASE/PRConfig/v1r10/options/Brunel/PRTEST-COLLISION10-1000evts.py

# Other repos
+ Connect to SL5, SL4 repositories
+ On kernel change: test CMS OpenData VM, in particular VBox integration

# Upgrade
+ Upgrade from last production release
