# Password Generator Program v1.1
# pgen
# Written by Dan "Anansi" Ambrogio
#
# Purpose: The program takes 2 base passwords and combines them with the
#   website they are to be used for to make a single, secure password
#   for each site. All the user has to remember is their passwords,
#   meaning the password they actually type into the website will be
#   more complex and difficult to crack than one they had to memorize.
#   It also eliminates shared passwords between sites, so someone who
#   finds out your Reddit password can't simply use it to access your
#   email.
#
#   Both 9- and 12-digit passwords can be created, at the user's 
#   discretion, to account for different websites' eccentricities.
#
#   One weakness this method has is that all passwords are hex values,
#   meaning that they consist of characters from 0-9 and a-f, A-F. Thus,
#   there are fewer possible combinations than a completely alphanumeric
#   password. Fortunately, an attacker would have to know that the letters
#   g-z and G-Z are not in use to gain an advantage.
#   Anyone improving upon this program would do well to change the method
#   of password generation to work around this weakness.

import string
import hashlib
import re

def check_pword(password):
    '''
    This function checks the generated password to make sure it complies
    to password standards. The generated password should have lowercase,
    uppercase, and numbers
    
    The 'password' variable is a string containing the password to be
    checked. The function returns True if it is a valid password.
    '''
    
    # Makes a string containing all the digits and upper/lower characters
    valid = (string.digits + string.ascii_lowercase +
             string.ascii_uppercase)


    # Checks that each character is a number or letter
    if any(i in valid for i in password):
        if (sum(b in string.digits for b in password)) > 0:
            if (sum(c in string.ascii_lowercase for c in password)) > 0:
                return True
    else: return False
    

def gen_pword(pass1, pass2, sitename, digits = 9, trial = 0):
    '''
    This function generates a password based on the two user passwords
    and the site.
    
    The 'pass1' variable is a string containing the first user password.
    The 'pass2' variable is a string containing the second user password.
    The 'sitename' variable is a string containing the website to generate
    the password for.
    The 'digits' variable is an integer containing the number of digits
    the password should have, 9 or 12
    The 'trial' variable is an integer used when the generated password
    does not meet standards; it increments the position in the hash to use
    to try again for a valid password.
    '''
    
    # Convert the passwords to SHA224 hashes and get the hex values
    pass1 = hashlib.sha224(bytearray(pass1, 'utf-8')).hexdigest()
    pass2 = hashlib.sha224(bytearray(pass2, 'utf-8')).hexdigest()
    sitename = hashlib.sha224(bytearray(sitename, 'utf-8')).hexdigest()
    
    # Take pseudorandom values from the hashes and combine them
    out = ""
    for i in range((digits//3)):
        out += pass1[1+i+trial]       # Picked at random
        out += pass2[30-i-trial]      # Same
        out += sitename[1+i+trial]    # Same
    
    # Convert the first lowercase letter to uppercase
    if (sum(c in string.ascii_lowercase for c in out)) > 1:
        # Note to self: learn what the hell this does.
        # Regular expressions AND lambdas. Ugh.
        out = re.sub('[a-z]', lambda x: x.group(0).upper(), out, 1)
    
    # Return the generated password
    return (out)


if __name__ == "__main__":
    # Program starts here
    
    # User-selected input
    p1, p2, site, length = '', '', '', ''
    
    # Program output
    output = ''
    
    # Print instructions for the user
    print( '\n\nPassword Generator Program v1.1' )
    print( 'Written by Dan "Anansi" Ambrogio')
    print( '________________________________\n' )
    print( 'This program creates a password for a website based on two' )
    print( "passwords and the website. For example: 'happy', 'smile'," )
    print( "and 'gmail'. This takes your two simple passwords, and gives")
    print( 'you a strong password for gmail.com. Now all you have to' )
    print( 'remember is your two simple passwords and what website' )
    print( "you're trying to access. Please note that punctuation" )
    print( "matters, so 'http://gmail.com' is not the same as 'gmail'\n")
    
    # User chooses 9 or 12 digit password
    while length == "":
        length = input( "First, would you like a 9- or 12-digit password?")
        
        try:
            if int(length) != 9 and int(length) != 12:
                length = ''
        except: 
            print ( "Please choose 9 or 12." )
            length = ''
    length = int(length)
           
    # User enters password 1
    while p1 == "":
        p1 = input( 'Enter your first password or q to quit: ' )
        if p1 == 'q' or p1 == 'Q': exit()
    
    while p2 == "":
        p2 = input( 'Enter your second password or q to quit: ' )
        if p2 == 'q' or p2 == 'Q': exit()
    
    while site == "":
        site = input( 'Enter the website or q to quit: ' )
        if site == 'q' or site == 'Q': exit()
    
    # Generates a password. Only exits the loop if the password
    # is marked as valid
    valid = False
    count = 0
    while valid == False:
        output = gen_pword(p1, p2, site, length, count)
        if (check_pword(output) == True): 
            valid = True
        else: count += 1
    
    print( 'Your new password is: {}'.format(output) )
    input( 'Press Enter to exit the program' )
    print (chr(27) + "[2J")     #Clears the screen
