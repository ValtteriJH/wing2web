import requests
import sys

import hashlib
from secAlg import getSecret

print(sys.argv)
def post(a,b, secret):
    response = requests.post(
        url=f'https://api.swider.dev/add?text={a} {b}',
        json={'crypt': secret
        }
    )
    
    print(response.content)


if len(sys.argv) == 3:
    a = sys.argv[1]
    b = sys.argv[2]
    secret = getSecret([a,b])
    post(a,b, secret)

else:
    a = '4'
    b ='20'
    secret = getSecret([a,b])
    post(a,b,secret)



