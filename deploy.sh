#!/bin/sh

python setup.py sdist
scp dist/* pi@192.168.1.100:~/packages

echo "Deploy done"