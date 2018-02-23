from os import path

from adb import adb_commands
from adb import sign_m2crypto
from adb import sign_pythonrsa

signer = sign_m2crypto.CrpytographySigner(
  path.expanduser('~/.android/adbkey')
)
# signer = sign_pythonrsa.PythonRSASigner(
#   pub=path.expanduser('~/.android/adbkey.pub'),
#   priv=path.expanduser('~/.android/adbkey')
# )

device = adb_commands.AdbCommands.ConnectDevice(
  auth_timeout_ms=3000,
  rsa_keys=[signer]
)

for i in xrange(10):
  print device.Shell('echo %d' % i)
