#!/bin/bash -e
if [ -z "$1" ]; then
  echo "Usage: build.sh version_number"
  exit 1
fi

version="$1"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS tmp || true
mkdir -p BUILD RPMS SRPMS

# real action happens here
rpmbuild -ba --define="_topdir $PWD" --define="_tmppath $PWD/tmp" --define="ver $version" SPECS/solr.spec
