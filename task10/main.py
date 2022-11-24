p = 11003378959096834724676546774061387323366640315376248759704778733861819318638880334019013198255253637201505215283454116581559061011493945035043282347726567
q = 13352889525665842987778367770008624367016738648357150498263337383873676994755016453139838515936896298380832735119884881555123452210776892442746292021125831
e = 65537
d = 69357425854335667435469380960551384845473529705172208755274378055130556220144321336280182386572376501722777078239543992605048261113781725370395014753635278111987701312950756882999549218951256463733424485080811858880863848299798658061367375851385442141410733493910441693585064588874291332393795622978366749253
n = p * q

def decrypt_RSA(message, e, n):
    """
    >>> decrypt_RSA(86570912637207688430658050442534138686860113447750593750129115867611069795980400149875084938172511059077111775763831984800728158009625476246509869646143906270016350813522907485120229804954044822840485338235665911639144492389863191230410694146471337610863228296869316878318424832455813948760206789878680061806,d,n)
    1412
    >>> decrypt_RSA(83815489698949425454503411340462271441833577560361070073340854340767697288862182622524598818990559851595417109271788865693175864183668088463270319213547090274280405302127646890044893707234611412838644930391470657208403905675470886164666899520786460799826428450507750448082240371010595240565614073056710598296,d,n)
    423523131313
    """
    return pow(message, d, n)

def encrypt_RSA(message, e, n):
    """
    >>> encrypt_RSA(1412,e,n)
    86570912637207688430658050442534138686860113447750593750129115867611069795980400149875084938172511059077111775763831984800728158009625476246509869646143906270016350813522907485120229804954044822840485338235665911639144492389863191230410694146471337610863228296869316878318424832455813948760206789878680061806
    >>> encrypt_RSA(423523131313,e,n)
    83815489698949425454503411340462271441833577560361070073340854340767697288862182622524598818990559851595417109271788865693175864183668088463270319213547090274280405302127646890044893707234611412838644930391470657208403905675470886164666899520786460799826428450507750448082240371010595240565614073056710598296
    >>> test_result = True
    >>> import random
    >>> for i in range(10):
    ...     test_case = random.randint(0,100000000000000000)
    ...     if decrypt_RSA(encrypt_RSA(test_case,e,n),d,n) != test_case:
    ...         test_result = False
    >>> test_result
    True
    """
    return pow(message, e, n)    

def find_the_correctly_encrypted():
    from suppl import ciphers # I saved the cipher in this file
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
    import base64
    
    # Read the list of keys to decrypt
    f = open('secret_key.pem', 'r')
    secret_key = RSA.import_key(f.read())
    
    for i in range(len(ciphers)):
        try:
            msg = PKCS1_OAEP.new(secret_key).decrypt(base64.b64decode(ciphers[i]))
        except: # If an error is thrown while decryption move on to the next one
            continue
        return msg.decode('ascii')    
    
def find_the_real_code():
    from suppl import messages
    from Crypto.PublicKey import RSA
    from hashlib import sha512
    import base64
    
    # Read the public RSA key
    f = open('my_friend_key.pub', 'r')
    key = RSA.import_key(f.read())
    
    for i in range(len(messages)):
        text = messages[i]['text']
        signature = messages[i]['signature']
        
        # Decode text
        conv_deco = text.decode('ascii')[12:]
        # Convert message
        conv_text = int.from_bytes(sha512(text).digest(), byteorder='big')
        # Convert signature
        conv_sign = pow(int.from_bytes(base64.b64decode(signature), byteorder='big'), key.e, key.n)
        
        if(conv_text == conv_sign):
            return conv_deco
    

if(__name__ == '__main__'):
    print('Correctly decrypted key:', find_the_correctly_encrypted())
    print('Find the real code: ', find_the_real_code())
    import doctest
    print(doctest.testmod())