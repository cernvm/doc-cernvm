# Running on Google Compute Engine

CernVM can be instantiated and contextualized on Google Compute Engine (GCE). Currently, only amiconfig contextualization is supported. By convention, amiconfig looks for Base64 encoded user data under the key cvm-user-data on the GCE meta data server.

The GCE client utilities are part of CernVM, so you can use an interactive CernVM to manage your GCE batch CernVMs. The following steps upload the image and start an instance on GCE:

  - Upload the GCE .tar.gz image to Google cloud storage with `gsutil cp <GCE IMAGE> gs://<BUCKET>/<GCE IMAGE>`
  - Add the image to you project with `gcutil addimage <IMAGE NAME> gs://<BUCKET>/<GCE IMAGE>`
  - Create an ssh keypair with `ssh-keygen -f <KEYPAIR>`

Start the instance with the user data in the file user-data:

    gcutil addinstance --image=<IMAGE NAME> --kernel="" <INSTANCE NAME> \
      --metadata=cvm-user-data:$(base64 -w0 user-data) \
      --authorized_ssh_keys=root:<KEYPAIR>.pub
