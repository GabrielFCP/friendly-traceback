#!/usr/bin/env bash
set -e
pip install build --quiet
python -m build --wheel --no-isolation
echo "Wheel built in dist/"
