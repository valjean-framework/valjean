#!/bin/bash
SPACK_ROOT=$1
if [ "x${SPACK_ROOT}" = x ]; then
  echo "usage: source spack-python.sh <SPACK_ROOT>"
  exit 1
fi

source "${SPACK_ROOT}/share/spack/setup-env.sh"
# generate a sanitized environment name (only letters, digits, - and _ allowed)
ENV_NAME=$(spack arch -o)
if [ "x${SUFFIX}" != x ]; then
  ENV_NAME="${ENV_NAME}-${SUFFIX}"
fi
ENV_NAME=$(echo "${ENV_NAME}" | tr -d '\n' | tr -c '[:alnum:]_-' _)

# load all the python modules; expecting to find them in the environment folder
for module in ${SPACK_ROOT}/var/spack/environments/${ENV_NAME}/modules-python@*; do
  source ${module}
done
