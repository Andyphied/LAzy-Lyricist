

def error_message(code=1):
    if code == 1:
        message = ['Could Not Generate New Lyrics For This Artist/Album as we could not find it']
        return message

    if code >= 500:
        message= ('[!] [{0}] Server Error'.format(code))
        return message

    elif code == 401:
        message= ('[!] [{0}] Authentication Failed'.format(code))
        return message
    elif code >= 400:
        message= ('[!] [{0}] Bad Request'.format(code))
        #message= (ssh_key )
        #message= (response.content )
        return message
    elif code >= 300:
        message= ('[!] [{0}] Unexpected redirect.'.format(code))
        return message
