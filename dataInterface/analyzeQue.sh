#! /usr/bin/bash
rpicam-jpeg --output /home/swider/Downloads/siibiRepo/testPics/curImg.jpg --timeout 2000 &
/home/swider/.venv/bin/python /home/swider/Downloads/siibiRepo/postPicture.py &
wait
