from random import randint
from datetime import datetime

def create_otp(size=6):
    start = int(10**(size-1)) # 100000 if size is 6
    end = int((10**size) - 1) # 999999 if size is 6
    token = str(randint(start, end))
    
    return token

def date_diff_in_secs(creation_date, entry_date):
    return int(abs((entry_date - creation_date).total_seconds()))

