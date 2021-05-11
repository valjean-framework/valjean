#!/bin/bash
umask 002
SPACK_ROOT=$1
if [ "x${SPACK_ROOT}" = x ]; then
  echo "usage: source spack-python.sh <SPACK_ROOT>"
  exit 1
fi

SPACK=$SPACK_ROOT/bin/spack

# generate a sanitized environment name (only letters, digits, - and _ allowed)
OS=$(${SPACK} arch -o)
if [ "x${SUFFIX}" != x ]; then
  ENV_NAME="${OS}-${SUFFIX}"
else
  ENV_NAME="${OS}"
fi
ENV_NAME=$(echo "${ENV_NAME}" | tr -d '\n' | tr -c '[:alnum:]_-' _)

# load all the python modules; expecting to find the script in the environment
# folder
source /etc/profile.d/modules.sh
module use ${SPACK_ROOT}/share/spack/modules/linux-${OS}-x86_64
source ${SPACK_ROOT}/var/spack/environments/${ENV_NAME}/loads
