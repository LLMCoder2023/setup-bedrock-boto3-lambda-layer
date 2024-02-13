#!/bin/bash
set -eo pipefail
mkdir -p python
pip3 install --target ./python -r requirements.txt
zip -r lambda-layer-python-sdk-1.34.39.zip ./python