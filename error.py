

def error_message(code=1):
    if code == 1:
        message = 'Could Not Generate New Lyrics For This Artist/Album as we could not find it'
        return message

    if code >= 500:
        print('[!] [{0}] Server Error'.format(code))
        return None

    elif code == 401:
        print('[!] [{0}] Authentication Failed'.format(code))
        return None
    elif code >= 400:
        print('[!] [{0}] Bad Request'.format(code))
        #print(ssh_key )
        #print(response.content )
        return None
    elif code >= 300:
        print('[!] [{0}] Unexpected redirect.'.format(code))
        return None
