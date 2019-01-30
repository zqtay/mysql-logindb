# Preparations
if True:
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA3_256
    import uuid, random
    import mysql.connector

# Functions
if True:
    def encryptregister(UN,PW):
        PWiter=random.randrange(20,500)
        PWsalt=uuid.uuid4().hex[:-3]+str(PWiter).zfill(3)
        PWsaltiter=random.randrange(20,500)
        PWsaltsalt=uuid.uuid4().hex[:-3]+str(PWsaltiter).zfill(3)
        hUN = SHA3_256.new(bytes(UN, encoding='utf-8')).hexdigest()
        cipher = AES.new(bytes(hUN[:16], encoding='utf-8'), AES.MODE_ECB)
        ePWsalt = bytes(PWsalt+PWsaltsalt, encoding='utf-8')
        for i in range(PWsaltiter):
            ePWsalt=cipher.encrypt(ePWsalt)
        ePWsalt=ePWsalt.hex()
        hPW=bytes(PW + PWsalt, encoding='utf-8')
        for i in range(PWiter):
            hPW=SHA3_256.new(hPW).digest()
        hPW=hPW.hex()
        return (hUN+PWsaltsalt+ePWsalt+hPW)

    def decryptlogin(UN, PW, code):
        hUN,PWsaltsalt,ePWsalt,hPW = [i for i in [code[x:y] for (x,y) in [(0,64),(64,96),(96,224),(224,288)]]]
        try:
            if SHA3_256.new(bytes(UN, encoding='utf-8')).hexdigest() == hUN:
                PWsaltiter=int(PWsaltsalt[-3:])
                cipher = AES.new(bytes(hUN[:16],encoding='utf-8'), AES.MODE_ECB)
                PWsalt = bytes.fromhex(ePWsalt)
                for i in range(PWsaltiter):
                    PWsalt = cipher.decrypt(PWsalt)
                PWsalt=PWsalt.decode('utf-8')[:32]
                PWiter=int(PWsalt[-3:])
                hPWin=bytes(PW + PWsalt, encoding='utf-8')
                for i in range(PWiter):
                    hPWin=SHA3_256.new(hPWin).digest()
                if hPWin.hex() == hPW:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def registerquery(code,info):
        return f"INSERT INTO `USERLOGIN` " \
               f"(`CODE`,`INFO`) " \
               f"VALUES (\'{code}\',\'{info}\');"

    def usernamequery(hUN):
        return f"SELECT `CODE` FROM `USERLOGIN` " \
               f"WHERE `CODE` LIKE \'{hUN}%\';"

# Database connection
if True:
    dbhostname = 'dbhostname'
    dbusername = 'dbusername'
    dbpassword = 'dbpassword'
    dbname = 'dbname'

    cxn = mysql.connector.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname)
    cxn.autocommit = True
    cursor = cxn.cursor()

# Prompt
if True:
    print("Authentication")
    LR=input('Log-in (L) or Register (R)?\n').upper()
    if LR == 'L' or LR == 'R':
        username=input('Please enter your username:\n')
        password=input('Please enter your password:\n')
        if len(username) in range(5,61) and len(password) in range(5,61):
            if LR == 'L':
                cursor.execute(usernamequery(SHA3_256.new(bytes(username,encoding='utf-8')).hexdigest()))
                matches=[code for code in cursor]
                if len(matches) == 1 and decryptlogin(username,password,matches[0][0]):
                    print('Log-in successful. Please enter any key to exit.')
                else:
                    print('Log-in failed. Please verify your log-in info.')
            elif LR == 'R':
                cursor.execute(usernamequery(SHA3_256.new(bytes(username,encoding='utf-8')).hexdigest()))
                if len([code for code in cursor]) == 0:
                    cursor.execute(registerquery(encryptregister(username,password),username+':'+password))
                    cursor.execute(usernamequery(SHA3_256.new(bytes(username,encoding='utf-8')).hexdigest()))
                    if len([code for code in cursor]) == 1:
                        print('Registration successful. Please enter any key to exit.')
                    else:
                        print('Registration failed. Please enter any key to exit.')
                else:
                    print('The username has already existed.')
        else:
            print('The username and password must be within the range of 6 to 50 characters!')
    else:
        print('Please enter a valid response (L or R)!')
    input()
