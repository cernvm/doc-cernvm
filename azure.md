# Running on Microsoft Azure

You can use the `azure` utility in CernVM to upload images to the Azure cloud storage and to control virtual machines.


## Setting Azure Credentials

In order to establish your account credentials, use

    azure account download
    azure account import <CREDENTIALS FILE>

and follow the instructions of the utility.


## Uploading the CernVM Image

For Azure, get the CernVM image in VHD format from the download page.  If you haven't done before, create a _storage account_ with

    azure storage account create <STORAGE ACCOUNT>

Otherwise, set the storage account with

    azure storage account set <STORAGE ACCOUNT>

Retrieve the storage _connection string_ and set it in your environemnt.  The `<ACCOUNT KEY>` refers to the last part of the connection string following `AccountKey=`.

    azure storage account connectionstring show <STORAGE ACCOUNT>
    export AZURE_STORAGE_CONNECTION_STRING="<CONNECTION STRING>"
    export AZURE_STORAGE_ACCESS_KEY="<ACCESS KEY>"

If you haven't done so, create a _container_ in your storage account with

    azure storage container create <CONTAINER>

Upload and create the image (you can pick `<IMAGE NAME>`) with

    azure vm disk upload <CERNVM IMAGE> \
      https://<STORAGE ACCOUNT>.blob.core.windows.net/<CONTAINER>/<IMAGE NAME>.vhd \
      $AZURE_STORAGE_ACCESS_KEY
    azure vm image create --os linux --blob-url \
      https://<STORAGE ACCOUNT>.blob.core.windows.net/<CONTAINER>/<IMAGE NAME>.vhd \
      <IMAGE NAME>


## Creating Virtual Machines

For Azure VMs, the ssh credentials are extraced from an X.509 certificate.  In order to create valid ssh credentials, use

    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout <KEY NAME>.key -out <CERT NAME>.pem
    chmod 600 <KEY NAME>.key

You can also create credentials from an existing SSH key with

    openssl req -x509 -key ~/.ssh/id_rsa -nodes -days 365 -newkey rsa:2048 -out <CERT NAME>.pem

These procedure is described in more detail in the [Azure Online Help](https://azure.microsoft.com/en-us/documentation/articles/virtual-machines-linux-use-ssh-key).

Virtual machine creation requires a user name and password, even if ssh credentials are provided.  We recommend to use `azure` for `<USER NAME>` and a throw-away password, for instance `"@Aa0$(cat /dev/urandom | tr -cd [:alnum:] | head -c24)"`.  Create the virtual machine with

    azure vm create <INSTANCE NAME> <IMAGE NAME> --ssh --ssh-cert <CERT NAME>.pem \
      --custom-data "./user-data" <USER NAME> <PASSWORD>

For ssh login, you can retrieve the public IP address of the image with

    azure vm show <INSTANCE NAME>

For help on creating the user-data file, see our [contextualization page](http://cernvm.cern.ch/portal/contextualisation).
