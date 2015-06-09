# Running on Amazon EC2

A pre-built bundle on Amazon S3 is publicly available. You can find it if you search for "CernVM" in the community provided AMIs. In order to successfully boot CernVM on EC2, it requires ephemeral storage being attached to the EC2 instance. You can use a CernVM 3 to manage your EC2 virtual machines; CernVM 3 already comes with the EC2 command line tools. To instantiate an EC2 machine from a CernVM 3 on your laptop, you can use for instance

    ec2-run-instances -n 1 -k <KEYPAIR> -t m1.small -f  -g default

**Note:** previously, we added the `-b /dev/sdc=ephemeral0` to this command.  As of CernVM 3.4 (uCernVM bootoader 2.0), this options must not be present.

For help on creating the user-data file, see our [contextualization page](http://cernvm.cern.ch/portal/contextualisation).

If you want to bundle and upload the image yourself, you can use the "Filesystem" format of the image. The image needs to be bundled with an [Amazon PV-GRUB](http://docs.aws.amazon.com/AWSEC2/2011-07-15/UserGuide/index.html?UserProvidedkernels.html) >= 1.04 kernel (e.g. aki-919dcaf8).  The EC2 commands to create and upload a bundle are roughly

    ec2-bundle-image -u <AWSACCOUNTID> -i <CERNVM IMAGE>.fat --debug --arch x86_64 --kernel aki-919dcaf8
    ec2-upload-bundle -m <CERNVM IMAGE>.fat.manifest.xml -b <S3 BUCKET>
    ec2-register -a x86_64 <S3 BUCKET>/<CERNVM IMAGE>.fat.manifest.xml  -d <DESCRIPTION>
