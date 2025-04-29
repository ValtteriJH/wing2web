from rapidocr_onnxruntime import RapidOCR

import requests
import sys
import hashlib
import os
from dotenv import load_dotenv

from secAlg import getSecret

import cv2



# Load .env file
load_dotenv()

# Access environment variables
IMGPATH = os.getenv("IMGPATH")


def post(a,b, secret):
    response = requests.post(
        url=f'https://api.swider.dev/add?text={a} {b}',
        json={'crypt': secret
        }
    )
    
    print(response.content)

engine = RapidOCR()

imgs = [IMGPATH]
imgpath = imgs[0]


# DOWNSAMPLE
img = cv2.imread(imgpath)

img = cv2.pyrDown(img)

# Convert the image to grayscale
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Save the grayscale image
cv2.imwrite(imgpath, img)



result, elapse = engine(imgpath)
outputs = []
valid = False
print(result)
for i in result:
    if len(i[1]) < 3 and len(i[1]) > 0:
        if i[1] != '?' and i[0] != 'N':
            outputs.append(i[1])

if len(outputs) == 2:
    valid = True
print(outputs)
if valid:
    print("is valid!")
    a = outputs[0]
    b = outputs[1]

    secret = getSecret(a,b)

    post(a,b, secret)

