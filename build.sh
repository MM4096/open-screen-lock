#!/usr/bin/env bash

cd "$(dirname "$0")" || exit 1

echo "Building main"
pyinstaller -F main.py -n OpenScreenLock -c >> /dev/null
chmod +x dist/OpenScreenLock
echo "Building time_notifier"
pyinstaller -F time_notifier.py -n OpenScreenLock-TimeNotifier -c >> /dev/null
chmod +x dist/OpenScreenLock-TimeNotifier
echo "Building background"
pyinstaller -F background.py -n OpenScreenLock-Background -c >> /dev/null
chmod +x dist/OpenScreenLock-Background