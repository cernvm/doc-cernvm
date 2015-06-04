CernVM Image Signatures
=======================

The HDD and ISO images of the CernVM bootloader are signed by the cvm-sign01.cern.ch host certificate.  At the end of the images, there is a 64kB signature block (`tail -c $((64*1024)) <image>`) which is ignored by the hypervisors.  The 64kB block is divided into two zero-padded 32kB blocks. The first block contains a JSON object with meta-data about the image, the second block contains the signature JSON object. The signature is on the image plus the first 32kB block.

The signature JSON object in the last 32kB signature block contains the base64 encoded strings "certificate" and "signature". There is also a "howto-verify" list of strings containing a few hints how to verify the signature with openssl.
