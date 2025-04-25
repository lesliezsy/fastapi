
from passlib.context import CryptContext

# to tell passlib to use bcrypt as the hashing algorithm
# bcrypt is a password hashing function
# CryptContext is a class that provides a way to hash and verify passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# this is to hash the password
def hash_password(password: str):
    return pwd_context.hash(password)

# this is to verify the password
# return True if the password is correct
# plain_password is the password entered by the user
# hashed_password is the password stored in the database
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
