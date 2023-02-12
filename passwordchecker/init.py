import requests
import hashlib
import sys

#Requests data from API 

def req_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error with code {res.status_code}')
    
    return res

# With the API's information, if there are any passwords with a number
#(signifying "compromised"), it will return that number, else it will return 0
   
def get_pwd_leaks(hashes, pwd_hash):
    hashes_tuple = (line.split(':') for line in hashes.text.splitlines())
    
    for h, count in hashes_tuple:
       
        if h == pwd_hash:
            return count
    
    return 0


    # for hash, count in hashes_tuple:
    #     pass

#Hashes password and sends to API to get a response

def check_api(password):
    sha1pwd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1pwd[:5], sha1pwd[5:]
    res = req_api_data(first5_char)

    return get_pwd_leaks(res, tail)

#main function

def main(args):
    print(args)
    for pwd in args:
        
        compromised = check_api(pwd)
        if compromised:
            print(f"Oh no, your password has been found {compromised} times!!")
        
        else:
            print("Your password has not been compromised yet!")


#While running this on the terminal, after init.py, put your pwd example
# ex: init.py examplepw
   
main(sys.argv[1:])