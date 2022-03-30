#a class for user and pass
import sqlite3
import re
from getpass import getpass
import smtplib


DataBaseName='PariDB'
UserPassDB='userpass'
TableName='PariTable'

# #path for creating a database for dictionary
pathDb='./{}.db'.format(DataBaseName)

# #path for creating a database for members' user and pass
pathDict='./{}.db'.format(UserPassDB)


class UserPass(object): 
    
    def _user_pass(foo):
        def wrapper (self,*args):
            MemberIdentification=input('''are you a member of this club?
            if your answer is YES enter 1 and if it is NO enter 2 ''').strip()
            MemberIdentification=int(MemberIdentification) if MemberIdentification.isdigit() else str(MemberIdentification)
            while MemberIdentification not in [1,2]:
                MemberIdentification=int(input("you should enter either 1 or 2").strip())
            else:
                if MemberIdentification==2:
                    print('\nsorry!:( you are not allowed to use this option, otherwise you are a member of this club\n')
                    BeAMember=input('\ndo you want to sign up for membership?\nif your answer is YES enter 1 and if is NO enter 2\n')
                    if BeAMember.isdigit():
                        BeAMember=int(BeAMember.strip())
                    while BeAMember not in [1,2]:
                        BeAMember=input('enter either (1) or (2):   ')
                        BeAMember=int(BeAMember) if BeAMember.isdigit() else str(BeAMember)
                    else:
                        if BeAMember==2:
                            print('\n OK!\n')
                            print(False)
                        else:
                            conn=UserPass.username_database(pathDict)
                            UserPass.username_table(conn)
                            UserPass.sign_up(conn)
                            authorID=UserPass.sign_in(conn)
                            print(True)
                else:
                    conn=UserPass.username_database(pathDict)
                    UserPass.username_table(conn)
                    authorID=UserPass.sign_in(conn)
                    print(True)
            x=foo(self,*args)
        return wrapper
    
    
            
################ creating a database for keeping members' user and pass ############    

    @classmethod
    def username_database(cls, pathDict):
        conn=None
        try:
            conn=sqlite3.connect(pathDict)
        except Error as er:
            self.logger(er)
        return conn 

################ creating a table for keeping members' user and pass ############ 
    
    @classmethod
    def username_table(cls,conn):
        c=conn.cursor()
        try:
            c.execute('''CREATE TABLE userpass 
                            (name varchar not null  , 
                             time date not null unique ,
                             authorID varchar not null unique ,
                             password varchar not null ,
                             Email varchar not null)''')
            conn.commit()
            print('the table has been created successfully!:)\n')
        except sqlite3.OperationalError as o:
            #status='the table has already exists'
            #print(status)
            pass
        except:
            print("something went wrong")

            
################ checking whether the ahthorID is unique or not ############        
   
    @classmethod
    def sign_up(cls,conn):
        name=(input('\nwhat is your name\n')).strip()
        print('\nenter an E-mail\n')
        while True:
            Email=(input()).strip()
            expr = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
            match_object = expr.match(Email)
            if match_object:
                print('Thank you!')
                break
            else:
                print('it is not in the form of an email')

        authorID=(input('\ncreate an ID\n')).strip() 
        cursor = conn.execute("SELECT authorID from userpass")
        ID_column = []
        for row in cursor:
            ID_column += row
        while authorID in ID_column:
                authorID=input("sorry! An author already registered with this ID, please create another one!")
        
        else:
           
            print('''\nenter a password. your password should contain
                      atleast one upper case and lower case letter, symbol and digit\n''')
            while True:
                password=getpass().strip()
                rules = [
                    r'(?P<symbol>[!@.#$%^&*])?',
                    r'(?P<digit>\d)?',
                    r'(?P<uppercase>[A-Z])?',
                    r'(?P<lowercase>[a-z])?'
                    ]

                rgx      = re.compile(r''.join(rules))
                checks   = rgx.match(''.join(sorted(password))).groupdict()
                problems = [k for k,v in checks.items() if v is None]
                if problems==[]:
                    break
                else:
                    print("your password should contain at least one ",end='')
                    for i in problems:
                        print(i,end='')
                        if problems.index(i) <len(problems)-1:
                            if problems.index(i) ==len(problems)-2:
                                print(" and ",end='')
                            else:
                                print(", ",end='')
                        else:
                            print(".",end='\n')

            query_str = '''INSERT INTO userpass (name, authorID, time, password, Email)
            VALUES( '{}', '{}', datetime('now'),'{}','{}')'''.format(name, authorID,password, Email) 
            try:
                cursor=conn.execute(query_str)
                print("registration has been made, successfully!:) \n")
                conn.commit()
            except:
                print("something went wrong!:( ")
    
    
################################ sign in #################################
    @classmethod
    def sign_in(cls, conn):
        authorID=input('\nplease enter your ID:  \n').strip()
        cursor = conn.execute("SELECT * from userpass WHERE authorID='{}'".format(authorID))
        ID_column = []
        for row in cursor:
            ID_column += row
        while authorID not in ID_column:
            key=int(input('''Sorry, we don\'t recognise this author ID, do you want 
            to enter another author ID ((1)) or sign up ((2))? ''').strip())
            while key not in [1,2]:
                key=int(input('''enter either (1) or (2):   ''').strip())
            else:
                if key==1:
                    authorID=input(':  ')
                    cursor = conn.execute("SELECT * from userpass WHERE authorID='{}'".format(authorID))
                    ID_column = []
                    for row in cursor:
                        ID_column += row
                    if authorID in ID_column:
                        break
                    else:
                        continue
                else:
                    UserPass.sign_up(conn)
                    break
        else:  
            name = conn.execute("SELECT name from userpass WHERE authorID='{}'".format(authorID))
            name_column = []
            for row in name:
                name_column += row
            name=name_column[0]
            password = conn.execute("SELECT password from userpass WHERE authorID='{}'".format(authorID))
            pass_column = []
            for row in password:
                pass_column += row
            password=pass_column[0]
            Email= conn.execute("SELECT Email from userpass WHERE authorID='{}'".format(authorID))
            Email_column = []
            for row in Email:
                Email_column += row
            Email=Email_column[0]
            check=getpass('dear {}, enter your password:  '.format(name)).strip()
            while password!=check:
                print('''the password is wrong, do you want us to send it to your Email?
                    enter ((1)) if yes and ((2)) if no!''')
                while True:
                    A=input().strip()
                    A=int(A) if A.isdigit() else str(A)
                    if A==1:  
                        UserPass.email_sender(password, Email) 
                        break
                    elif A==2:
                        check=getpass("enter your password: ").strip()
                        break
                    else:
                        print("enter either 1 or 2")
                        continue
            else:
                print("welcome {}".format(name))
            
            
 #sending E-mails
    @classmethod
    def email_sender(cls, password, Email):
        TO =Email
        SUBJECT = 'Password'
        TEXT = 'Here is a message from dictionary.\n Your password is: {}'.format(password)

        # Gmail Sign In
        gmail_sender = 'python.practise1@gmail.com'
        gmail_passwd = 'ForooghKarimi1'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_sender, gmail_passwd)

        BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])
        
        try:
            server.sendmail(gmail_sender, [TO], BODY)
            print ('\n',20*'*','the password has been sent to your email address',20*'*','\n')
        except:
            print ('\n',20*'*','error sending mail',20*'*','\n')

        server.quit()       



#************************************************************************************************************


class ForooghDict:

############################# initialization ############################

    def __init__(self,word, definition, authorID):
        self.word=word
        self.definition=definition
        self.authorID=authorID

############################# reporting #################################        
    
    def logger(self,status):
        print('\n', 20 * "-", "\n", status, "\n", 20 * "-")
        
        
################### connecting to the database ###########################
    
    def ConnectionToDB(self,pathDb):
        conn=None
        try:
            conn=sqlite3.connect(pathDb)
            #print('the connection has been made successfully!:)\n')
        except Error as er:
            self.logger(er)
        return conn
    
######################## creating the table ###############################    
    
    def create_table(self, conn):
        c=conn.cursor()
        try:
            c.execute('''CREATE TABLE {} 
                            (word varchar not null unique ,
                             definition varchar not null , 
                             time date not null unique ,
                             authorID varchar not null)'''.format(TableName))
            conn.commit()
            self.logger('the table has been created successfully!:)\n')
        except sqlite3.OperationalError as o:
            status='the table has already exists'
            self.logger(status)
        except:
            print("something went wrong")    
            
########################## showing the dicionary############################           
                
    def show_dict(self, conn):
        cursor = conn.execute("SELECT word, definition, time, authorID from {}".format(TableName))
        for row in cursor:
            print("word = ", row[0])
            print("definition = ", row[1])
            print("time = ", row[2])
            print("authorID = ", row[3], "\n")
        self.logger('\n done!')

               
########################## deleting the table ###############################
               
    def delete_table(self,conn):
        c=conn.cursor()
        c.execute("DROP TABLE {}".format(TableName))
        self.logger("the table has been deleted!:(")
        conn.commit()

        
########################### inserting new words #############################
    @UserPass._user_pass     
    def insert_words(self,conn, word, definition, authorID):
        if UserPass._user_pass==False:
            print('not allowed')
        else:
            query_str = '''INSERT INTO {3} (word, definition, time, authorID)
                VALUES( '{0}', '{1}', datetime('now'),'{2}')'''.format(word.strip(), definition.strip(), authorID.strip(), TableName)

            try:
                conn.execute(query_str)
                print("\nthe word has been inserted!:)\n")
                conn.commit()
            except sqlite3.IntegrityError as e:
                self.logger('there is a similar word in the dictionary, please look it up')
            except:
                self.logger('something went wrong')

########################### deleting words ##################################
    @UserPass._user_pass
    def delete_words(self,conn, word_str):
        if UserPass._user_pass==False:
            print('not allowed')
        else:
            cur=conn.cursor()
            with conn:
                cursor = conn.execute("SELECT word from {}".format(TableName))
                word_column = []
                for row in cursor:
                    word_column += row
                if word_str in word_column:
                    result = cur.execute("DELETE FROM {1} WHERE word= '{0}'".format(word_str.strip(),TableName))
                    self.logger('the word has been deleted!')
                    conn.commit()
                else:
                    self.logger("the word does not exist!:(")


########################### look up words ##################################


    def lookup_word(self, conn,word_str):
            cursor = conn.execute("SELECT word from {}".format(TableName))
            word_column = []
            for row in cursor:
                word_column += row
            if word_str in word_column:
                cursor = conn.execute("SELECT * from {1} WHERE word='{0}'".format(word_str.strip(),TableName))
                for row in cursor:
                    print("word = ", row[0])
                    print("definition = ", row[1])
                    print("time = ", row[2])
                    print("authorID = ", row[3], "\n")
            else:
                self.logger("the word does not exist")

                
########################### look up words ##################################

    @UserPass._user_pass
    def modify_word(self, conn, word_str, new_def, new_authorID):
        A=UserPass._user_pass
        if A==False:
            self.logger('not allowed')
        else:
            cursor = conn.execute("SELECT word from {}".format(TableName))
            word_column = []
            for row in cursor:
                word_column += row
            if word in word_column:
                query_str= """
                    UPDATE {2}
                    SET definition = '{0}'
                    WHERE word = '{1}'
                    """.format(new_def.strip(),word_str.strip(), TableName)
                conn.execute(query_str)
                query_str1 = """
                        UPDATE {2}
                        SET authorID='{0}'
                        WHERE word = '{1}'
                        """.format(new_authorID, word_str, TableName)
                conn.execute(query_str1)
                self.logger('the word has been modified')
                conn.commit()

            else:
                self.logger("the word does not exist!:(")



#**************************************************************************************************************
import sqlite3
import time
import pprint


menu = '''
    Menu:

    1.show dict
    2.insert new word
    3.delete word
    4.search
    5.modify
    6.exit\n
'''
words_dict = {}
obj=ForooghDict(" "," "," ")
 
while True:
    print(menu)
    key_num = input("please Enter A Number Based On the Menu:\n").strip()

#read_file
    if key_num == "1":
        conn =obj.ConnectionToDB(pathDb)
        obj.show_dict(conn)

    # insert
    elif key_num == "2":
        conn =obj.ConnectionToDB(pathDb)
        word = input("please enter the word: \n")
        definition = input("what is the definition \n")
        authorID = input("enter your author id?:\n")
        obj.insert_words(conn, word.strip(), definition.strip(), authorID.strip())

    # delete
    elif key_num == "3":
        conn =obj.ConnectionToDB(pathDb)
        word = input("enter the word you want to delete: \n")
        obj.delete_words(conn, word.strip())

    # search
    elif key_num == "4":
        conn =obj.ConnectionToDB(pathDb)
        word = input("enter the name of ??: \n")
        obj.lookup_word(conn,word.strip())

    # modify
    elif key_num == "5":
        conn =obj.ConnectionToDB(pathDb)
        word=input('enter the word you want to midify: \n').strip()
        definition=input('enter the new definition for the word: {}\n'.format(word)).strip()
        authorID=input('enter your autor ID:\n')
        obj.modify_word(conn, word.strip(), definition.strip(), authorID.strip())
