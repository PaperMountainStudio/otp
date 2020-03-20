#!/usr/bin/env python3
import os
import pyotp
import subprocess
import sys
# idea: ~/.otp/github.gpg stores a OTP secret key for github
# the file is GPG encypted
# for example command "otp github" will give you a otp code
if len(sys.argv) != 2:
    print("usage: otp [name]")
    sys.exit(1)

account=sys.argv[1]
result = subprocess.Popen(["gpg2", "-d", f'{os.getenv("HOME")}/.otp/{account}.gpg'], stdout=subprocess.PIPE).stdout.read()
secret = result.decode("utf-8").replace("\n","")

totp = pyotp.TOTP(secret)
print(totp.now())
