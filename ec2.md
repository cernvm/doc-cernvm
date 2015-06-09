# Running on Amazon EC2

A pre-built bundle on Amazon S3 is publicly available. You can find it if you search for "CernVM" in the community provided AMIs. In order to successfully boot CernVM on EC2, it requires ephemeral storage being attached to the EC2 instance. You can use a CernVM 3 to manage your EC2 virtual machines; CernVM 3 already comes with the EC2 command line tools. To instantiate an EC2 machine from a CernVM 3 on your laptop, you can use for instance

    ec2-run-instances -n 1 -k <KEYPAIR> -t m1.small -f <USER DATA> -g default <AMI>

**Note:** previously, we added the `-b /dev/sdc=ephemeral0` to this command.  As of CernVM 3.4 (uCernVM bootoader 2.0), this options must not be present.

For help on creating the user-data file, see our [contextualization page](http://cernvm.cern.ch/portal/contextualisation).

If you want to bundle and upload the image yourself, you can use the "Filesystem" format of the image. The image needs to be bundled with an [Amazon PV-GRUB](http://docs.aws.amazon.com/AWSEC2/2011-07-15/UserGuide/index.html?UserProvidedkernels.html) >= 1.04 kernel (e.g. aki-919dcaf8).  The EC2 commands to create and upload a bundle are roughly

    ec2-bundle-image -u <AWSACCOUNTID> -i <CERNVM IMAGE>.fat --debug --arch x86_64 --kernel aki-919dcaf8
    ec2-upload-bundle -m <CERNVM IMAGE>.fat.manifest.xml -b <S3 BUCKET>
    ec2-register -a x86_64 <S3 BUCKET>/<CERNVM IMAGE>.fat.manifest.xml  -d <DESCRIPTION>


## EBS Backed Instances

In general we recommend using instance-store backed instances as described above. If you want to use EBS backed instances instead (e.g. because they total cost turns out to be lower), the following steps are necessary to prepare the volumes and the image.  These steps can be performed with the EC2 command line utilities in CernVM.

First import the CernVM "Filesystem" image for Amazon from the CernVM download page into a minimally sized (1G) EBS volume:

    ec2-import-volume -f raw -s 1 -z us-east-1a -b <S3 BUCKET> \
      -o <S3 ACCESS KEY> -w <S3 SECRET KEY> cernvm-3.4.3.fat

Other zones for the `-z` parameter can be listed with `ec2-describe-availability-zones`.  Use `ec2-describe-conversion-tasks` to get the import task id and to check when the import task finished.  Once finished, remove the intermediate image manifest in the S3 bucket with

    ec2-delete-disk-image -t <IMPORT TASK ID>

Use `ec2-describe-volumes` to get the volume id of the imported volume and create a snapshot with

    ec2-create-snapshot <IMAGE VOLUME ID>

In addition to the image volume, create a scratch volume (e.g. with 25G) and a scratch snapshot using

    ec2-create-volume -s 25 -z us-east-1a
    ec2-create-snapshot <SCRATCH VOLUME ID>

Register an EBS backed image with

    ec2-register -a x86_64 -n <NAME> -d <DESCRIPTION> -s <IMAGE SNAPSHOT ID> --kernel aki-919dcaf8

You can use a [different PV-GRUB kernel]((http://docs.aws.amazon.com/AWSEC2/2011-07-15/UserGuide/index.html?UserProvidedkernels.html)) for other availability zones.  Start instances for the new image with

    ec2-run-instances -b /dev/vdb=<SCRATCH SNAPHSOT ID> -n 1 -t m1.medium \
      -k <KEYPAIR> -f <USER DATA> -g default <AMI>

**Note on instance types:** this recipe currently does not work for m1.small and c1.medium instances types which [automatically attach a swap volume](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html#InstanceStoreSwapVolumes). The CernVM bootloader mistakenly takes this swap partition as a scratch space.  This [will be fixed](https://sft.its.cern.ch/jira/browse/CVM-863) in a future release.
