#!/bin/bash
umask 002
SPACK_ROOT=$1
PYTHON_VERSION=$2
if [ "x${SPACK_ROOT}" = x ]; then
  echo "usage: source spack-python.sh <SPACK_ROOT>"
  exit 1
fi

SPACK=$SPACK_ROOT/bin/spack

OS=$(${SPACK} arch -o)
# PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}{sys.version_info.minor}")')
PYTHON_VERSION=${PYTHON_VERSION/./}
if [ "x${SUFFIX}" != x ]; then
  ENV_NAME="${OS}_python${PYTHON_VERSION}-${SUFFIX}"
else
  ENV_NAME="${OS}_python${PYTHON_VERSION}"
fi
ENV_NAME=$(echo "${ENV_NAME}" | tr -d '\n' | tr -c '[:alnum:]_-' _)
# load all the python modules; expecting to find the script in the environment
# folder
source /etc/profile.d/modules.sh
module use ${SPACK_ROOT}/share/spack/modules/linux-${OS}-x86_64
source ${SPACK_ROOT}/var/spack/environments/${ENV_NAME}/loads
