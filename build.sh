#!/bin/bash -e

EXPECTED_ARGS=2
E_BADARGS=65

if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: build.sh version_number release_number"
  exit $E_BADARGS
fi

version="$1"
release="$2"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS tmp || true
mkdir -p BUILD RPMS SRPMS

# real action happens here
rpmbuild -ba --define="_topdir $PWD" --define="_tmppath $PWD/tmp" --define="ver $version" --define="rel $release" SPECS/solr.spec
