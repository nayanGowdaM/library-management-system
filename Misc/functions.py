# hashlib is used for secure hash and message digest functions, and binascii is used for converting between binary and ASCII.
# timeago is used for generating human-readable time differences, and datetime is used for manipulating dates and times.

import hashlib, binascii
import timeago, datetime


# A salt is a random value added to the password before hashing to prevent precomputed hash attacks.
salt=b'$#0x--.\'/\\98' 

# Hash a string based on some algo
def hash(string):
    dk = hashlib.pbkdf2_hmac('sha256', b'password', salt, 100000) #Uses the PBKDF2 HMAC algorithm with SHA-256 to hash the password.
    return binascii.hexlify(dk).decode("utf-8") #Converts the hashed bytes to a hex string and decodes it to a UTF-8 string for readability.

def b_hash(string):
    dk = hashlib.pbkdf2_hmac('sha256', b'password', salt, 100000)
    return binascii.hexlify(dk)
    
def ago(date):
    """
        Calculate a '3 hours ago' type string from a python datetime.
    """
    now = datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)

    return (timeago.format(date, now)) # will print x secs/hours/minutes ago