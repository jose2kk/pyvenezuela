#!/usr/bin/env bash

set -e
set -x

# mypy pyvenezuela
ruff check pyvenezuela tests scripts
ruff format pyvenezuela tests --check
