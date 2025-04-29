#! /usr/bin/bash

source .env

rpicam-jpeg --output $IMGPATH --timeout 1000 --width 540 --height 700 --shutter 20000;$PYPATH $POSTSCRIPTPATH
