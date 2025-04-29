#! /usr/bin/bash

source .env

rpicam-jpeg --output $IMGPATH --timeout 2000 &
$PYPATH $POSTSCRIPTPATH &
wait
