# Running on KVM

CernVM images for [KVM](http://www.linux-kvm.org/) (Kernel-based Virtual Machine) are intended to be used by experienced users, or by system administrators. For creating and controlling virtual machines with KVM we recommend using libvirt (in particular `virsh` command line utility) and virt-manager graphical tool.

## Prerequisies

  - Make sure that your host supports kvm (the output of the command should not be empty)
```
    > egrep '(vmx|svm)' --color=always /proc/cpuinfo
```
  - Make sure that you have kvm, bridge-utils, libvirt, and virt-manager packages installed.  The output of the following commands should not be empty.
```
    > lsmod | egrep 'kvm(_intel|_amd)'
    > brctl --version
    > virsh --version
    > virt-manager --version # (only for graphical interface)
```
  - Make sure that the permissions of /dev/kvm file are set to 0660 (or more open). The file should be owned by "root", and the group ownership should be set to "kvm"
```
    > ls -al /dev/kvm
    crw-rw---- 1 root kvm 10, 232 Oct 19 14:49 /dev/kvm
```
  - Make sure that KVM network is properly set up for using NAT
```
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
```

## Creating a Virtual Machine

Download CernVM ISO image from [CernVM Downloads page](/portal/downloads). CernVM 3 requires an empty hard drive as a persistent CernVM-FS cache. Create a sparse hard disk image file with dd:

    dd if=/dev/zero of=cernvm-hd.img bs=1 count=0 seek=20G

Create a virtual machine definition file for `virsh` (libvirt guest domain management interface), which should contain the following:

  - Virtual machine name
  - Memory size (in MB)
  - Number of virtual CPUs
  - Type of architecture ('x86_64') and boot device ('cdrom')
  - Hard drive and CD-ROM definition
  - Network interface definition
  - Graphical device definition

Example virtual machine definition file looks like this:

    <domain type='kvm'>
            <name>CernVM-3</name>
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
                            <source file='/data/test/ucernvm-prod.1.16-3.cernvm.x86_64.iso' />
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

Virtual machine is created with the following command:

    > virsh create vm-definition.xml

Virtual machines can be listed, started, stopped, and removed with:

    > virsh list
     Id Name                 State
    ----------------------------------
     5  CernVM-3             running

    > virsh shutdown CernVM-3
    Domain CernVM-3 is being shutdown

    > virsh start CernVM-3
    Domain CernVM-3 started

    > virsh destroy CernVM-3
    Domain CernVM-3 destroyed

Virtual machine console can be opened using the `virt-manager` program.
