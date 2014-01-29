#!/bin/sh

URL=http://cernvm.cern.ch/releases
VERSION=3.1.0
UVERSION=1.16-3
ARCH=x86_64
ARCHTYPE=64
STATUS=1
BUILDID=0
BRANCH=prod

BASEDIR=ucernvm-images.${UVERSION}.cernvm.${ARCH}

FORMATS="ISO@(VirtualBox)|iso ISO@(VMware)|iso Raw@(QEMU,KVM)|hdd HyperV@(Hyper-V)|vhd Filesystem@(Xen)|fat"

echo Content-type: text/plain
echo ""
for f in $FORMATS; do
  NAME=$(echo "$f" | cut -d'|' -f1 | tr '@' " ")
  SUFFIX=$(echo "$f" | cut -d'|' -f2)
  FILENAME="${BASEDIR}/ucernvm-${BRANCH}.${UVERSION}.cernvm.${ARCH}.${SUFFIX}"
  SIZE=$(stat -c %s "${FILENAME}")
  HASH=$(cat ${FILENAME}.sha256 | awk '{print $1}')
  
  echo "${BUILDID};${VERSION};${STATUS};${ARCHTYPE};${URL}/${FILENAME};${NAME};${NAME};${SIZE};${HASH};${URL}/${BASEDIR}"
done

