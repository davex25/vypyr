#!/usr/bin/bash

aclocal
autoconf
automake
./configure && cd src && ./setup.py install --user

