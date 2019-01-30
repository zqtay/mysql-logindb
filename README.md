# mysql-logindb
A practice of using Python as a login interface and a data encryption tool, and MySQL as a login credentials database.

## Encryption (Registration) route:
1. Randomise salts and iteration numbers and merge them in single salt string (PWsaltsalt & PWsalt)
2. Hash UserName (1 iteration, no salt)
3. Encrypt PWsalt (key = hUN[:16], iter = get from PWsaltsalt, salt = PWsaltsalt)
4. Hash PassWord (iter = get from PWsalt, salt = PWsalt)
5. Concatenate code (hUN + PWsaltsalt + ePWsalt + hPW)

## Decryption (Log-in) route:
1. Get code and unpack into hUN, PWsaltsalt, ePWsalt, hPW
2. Match hashed UserName input to hUN
3. Decrypt ePWsalt with salt and iteration number from PWsaltsalt
4. Hash PassWord input with salt and iteration number from decrypted PWsalt
5. Match hashed PassWord input to hPW

## Pseudo-code for variable assignment:
hashed UserName = SHA3_256(b'UserName', iter=1).hexdigest()

PassWord's salt's salt = random_uuid.hex[:-3] + str(random_number_of_encrypting_iterations.zeropad)

Password's salt = random_uuid.hex[:-3] + str(random_number_of_encrypting_iterations.zeropad)

encrypted PassWord's salt = AES(b'PWsalt+PWsaltsalt', key=hUN[:16], iter=int(PWsaltsalt[-3:]))

hashed PassWord = SHA3_256(b'PassWord+PWsalt', iter=int(PWsalt[:-3])).hexdigest()

len(key) = hUN(64)+PWsaltsalt(32)+ePWsalt(128)+hPW(64) = 288

## MySQL table:
CREATE TABLE `USERLOGIN` (

`ID` SMALLINT(5) UNSIGNED NOT NULL AUTO_INCREMENT,

`CODE` TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,

`INFO` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'For testing only');
