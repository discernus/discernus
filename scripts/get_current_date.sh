#!/bin/bash

# Utility script to get current date for documentation
# Usage: 
#   ./scripts/get_current_date.sh           # Returns: June 11, 2025
#   ./scripts/get_current_date.sh iso       # Returns: 2025-06-11
#   ./scripts/get_current_date.sh timestamp # Returns: 2025-06-11 08:49:35

case "$1" in
    "iso")
        date "+%Y-%m-%d"
        ;;
    "timestamp")
        date "+%Y-%m-%d %H:%M:%S"
        ;;
    "")
        date "+%B %-d, %Y"
        ;;
    *)
        echo "Usage: $0 [iso|timestamp]"
        echo "  (no args)  - Returns: June 11, 2025"
        echo "  iso        - Returns: 2025-06-11"
        echo "  timestamp  - Returns: 2025-06-11 08:49:35"
        exit 1
        ;;
esac 