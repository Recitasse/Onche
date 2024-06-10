import os
import json
import base64
import sys

from random import randint
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

from config.Variables.variables import *

from dataclasses import dataclass


@dataclass(init=False)
class Encrypteur:
    def _generate_key(self, password: str, salt: str) -> bytes:
        """Génère la clef"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode(),
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_file(self, path_in: str, salt: str, password: str) -> None:
        """Encrypte le fichier d'entré"""
        encryted_data = None
        key = self._generate_key(password, salt)
        cipher_suite = Fernet(key)
        if path_in.endswith(".json"):
            with open(path_in, "r") as fi:
                data = json.load(fi)
            encryted_data = cipher_suite.encrypt(json.dumps(data).encode())
        
        pos = randint(100, 4000)
        with open(path_in, "wb") as enc_fo:
            enc_fo.write(encryted_data[:pos]+salt.encode()+encryted_data[pos:])

    def decrypte_file(self, path_in: str, salt: str, password: str) -> dict:
        with open(path_in, "rb") as enc_fi:
            data = enc_fi.read()
            enc = ''.join(data.decode().split(salt)).encode()
        
        key = self._generate_key(password, salt)
        cipher_suite = Fernet(key)
        dec = cipher_suite.decrypt(enc)

        if path_in.endswith(".json"):
            return json.loads(dec.decode())
        return {}
