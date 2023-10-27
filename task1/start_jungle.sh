#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sclang $SCRIPT_DIR/jungle_scd.scd &

python3 $SCRIPT_DIR/interface.py