#!/usr/bin/env bash

set -e
set -x

ruff check pyvenezuela tests
ruff format pyvenezuela tests --check
ty check pyvenezuela
