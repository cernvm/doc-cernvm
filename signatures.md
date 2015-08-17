CernVM Image Signatures
=======================

The HDD and ISO images of the CernVM bootloader are signed by the cvm-sign01.cern.ch host certificate.  At the end of the images, there is a 64kB signature block (`tail -c $((64*1024)) <image>`) which is ignored by the hypervisors.  The 64kB block is divided into two zero-padded 32kB blocks. The first block contains a JSON object with meta-data about the image, the second block contains the signature JSON object. The signature is on the image plus the first 32kB block.

The signature JSON object in the last 32kB signature block contains the base64 encoded strings "certificate" and "signature". There is also a "howto-verify" list of strings containing a few hints how to verify the signature with openssl.

In order to verify the image signature, you can use the following steps

    tail -c $((64*1024)) <IMAGE>
    # write JSON contents of "certificate" to encoded_certificate using text editor
    # write JSON contents of "signature" to encoded_signature using text editor
    base64 -d encoded_certificate > certificate
    base64 -d encoded_signature > signature
    openssl verify -CApath <X509_CERT_DIR> certificate
    openssl x509 -in certificate -subject -noout # make sure output matches DN of cvm-sign01.cern.ch certificate
    openssl x509 -in certificate -pubkey -noout > pubkey
    head -c -32768 <IMAGE> > signed_image
    openssl dgst -sha256 -verify pubkey -signature signature signed_image 
