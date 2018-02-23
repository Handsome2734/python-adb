# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from adb import adb_protocol

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class M2CryptoSigner(adb_protocol.AuthSigner):
  """AuthSigner using M2Crypto."""

  def __init__(self, rsa_key_path):
    from M2Crypto import RSA
    with open(rsa_key_path + '.pub') as rsa_pub_file:
      self.public_key = rsa_pub_file.read()

    self.rsa_key = RSA.load_key(rsa_key_path)

  def Sign(self, data):
    
    return self.rsa_key.sign(data, 'sha1')

  def GetPublicKey(self):
    return self.public_key


class CrpytographySigner(adb_protocol.AuthSigner):

  def __init__(self, rsa_key_path):
    with open(rsa_key_path + '.pub') as rsa_pub_file:
      self.public_key = rsa_pub_file.read()

    with open(rsa_key_path, 'rb') as key_file:
      self.rsa_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
      )
  
  def Sign(self, data):
    return self.rsa_key.sign(
      data,
      padding.PKCS1v15(),
      hashes.SHA1()
    )

  def GetPublicKey(self):
    return self.public_key
