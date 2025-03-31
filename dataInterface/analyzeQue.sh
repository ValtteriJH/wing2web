#! /usr/bin/bash
rpicam-jpeg --output /home/*****/Downloads/siibiRepo/testPics/curImg.jpg --timeout 2000 &
/home/******/.venv/bin/python /home/*****/Downloads/siibiRepo/postPicture.py &
wait
