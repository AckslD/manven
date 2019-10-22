#!/usr/bin/env fish

# Get path to files
set MANVEN_PATH (python3 -m manven)

# Run the command
python3 $MANVEN_PATH/cli.py $argv

# Source anything that needs to be sourced
source $MANVEN_PATH/.to_execute.sh
