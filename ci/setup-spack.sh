#!/bin/bash

SRC=$1
SPACK_ROOT=$2

for i in $(grep "py{" ${SRC}/pyproject.toml | grep -o -E '[0-9]+')
do
    echo "source "${SRC}"/ci/spack-python.sh "${SPACK_ROOT}" "$i
    source ${SRC}/ci/spack-python.sh ${SPACK_ROOT} $i
done
