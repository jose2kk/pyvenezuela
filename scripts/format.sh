#!/bin/sh -e
set -x

ruff check pyvenezuela tests docs_src scripts --fix
ruff format pyvenezuela tests docs_src scripts
