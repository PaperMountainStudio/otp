#!/usr/bin/env python3
import os
import subprocess
import sys
import time
import base64
import struct
import hmac
from pathlib import Path
# idea: ~/.otp/github.gpg stores a OTP secret key for github
# the file is GPG encypted
# for example command "otp github" will give you a otp code

if len(sys.argv) != 2:
    print("usage: otp [name]")
    sys.exit(1)

account = sys.argv[1]

secretfile = Path(f'{os.getenv("HOME")}/.otp/{account}.gpg')
if not secretfile.is_file():
    print("secret not found")
    sys.exit(1)

result = subprocess.Popen(["gpg2", "-d", secretfile],
    stdout=subprocess.PIPE).stdout.read()
secret = result.decode("utf-8").replace("\n", "")


# hotp and totp functions are taken from https://github.com/susam/mintotp
def hotp(key, counter, digits=6, digest='sha1'):
    key = base64.b32decode(key.upper() + '=' * ((8 - len(key)) % 8))
    counter = struct.pack('>Q', counter)
    mac = hmac.new(key, counter, digest).digest()
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-digits:].rjust(digits, '0')


def totp(key, time_step=30, digits=6, digest='sha1'):
    return hotp(key, int(time.time() / time_step), digits, digest)

print(totp(secret))
