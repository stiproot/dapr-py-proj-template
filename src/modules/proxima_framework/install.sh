#!/bin/bash

# USED TO INSTALL THE PACKAGE LOCALLY.
# !!! THIS IS A TMP SOLUTION UNTIL WE PUBLISH TO OUR PIP FEED.

python -m pip uninstall tmpl_framework
python3.11 -m pip uninstall tmpl_framework
python3.12 -m pip uninstall tmpl_framework

python -m pip install dist/tmpl_framework-0.0.1/.
python3.11 -m pip install dist/tmpl_framework-0.0.1/.
python3.12 -m pip install dist/tmpl_framework-0.0.1/.

cp -f dist/tmpl_framework-0.0.1.tar.gz ~/code/azdo/Internal-Proxima/src/upload-worker/pkgs/
cp -f dist/tmpl_framework-0.0.1.tar.gz ~/code/azdo/Internal-Proxima/src/workflows-worker/pkgs/
cp -f dist/tmpl_framework-0.0.1.tar.gz ~/code/azdo/Internal-Proxima/src/receipts-worker/pkgs/
cp -f dist/tmpl_framework-0.0.1.tar.gz ~/code/azdo/Internal-Proxima/test/test-harness/pkgs/