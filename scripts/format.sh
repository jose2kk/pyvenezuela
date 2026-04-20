#!/usr/bin/env bash

set -e
set -x

ruff format pyvenezuela tests
ruff check pyvenezuela tests --fix
