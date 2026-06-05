import getpass
passwords = {}
passes = []
password = ''
accounts = []
def random_password():
    '''
    random_password() is used to generate random password.
    The length of the password is dicided by the users.
    Parameter:no
    return:
    A string of randomly generated password 
    '''
    import random
    import string
    password =''
    while True:
        digit=input("Enter the length of the password:")
        int_list = []
        sum1 = 0
        numstring_list = [str(i) for i in range(10)]
        int_list.extend(''.join(digit))
        for i in int_list:
            if i in numstring_list:
                sum1+=1
        if sum1 ==len(int_list):
            digit = int(digit)
            break
        else:
            print("\nError!Please enter a number.\n")
    letter = []
    for i in range(65,91):
        letter.append(chr(i))
    for i in range(97,123):
        letter.append(chr(i))
    number = [0,1,2,3,4,5,6,7,8,9]
        
    punctuation =[]
    punctuation.extend(''.join(string.punctuation))
    combine_list = (letter+number+punctuation)*digit
            
            
    password = random.sample(combine_list, digit)

    password_middle = [str(i) for i in password]
    password_end = ''.join(password_middle)
        
    return password_end

def analysis(password):
    '''
    analysis(password) is used to analyse password strength.
    Judgment rules are shown in the report.
    Parameter:
    the password string
    return:
    the critical results: very strong, strong, medium, commonly or weak
    '''
    num = 0
    password_list = []
    password_list2 = []
    number =[s for s in range(48,58)]
    upper =[k for k in range(65,91)]
    lower =[u for u in range(97,123)] 
    password_list.extend("".join(password))
    if password =='':
        return
    else:
        for i in password_list:
            password_list2.append(ord(i))
    #length        
        score = 0
        if 5<=len(password)<=7:
            score+=5
        elif len(password)>=8:
            score+=10
    #symbol
        punctuation = []
        for item in password_list2:
            if item not in number and item not in upper and item not in lower:
                punctuation.append(item)
        if len(punctuation)==1:
            score+=5
            num+=1
        elif len(punctuation)>1:
            score+=15
            num+=1
    #number
        number1 =[]
        
        for q in password_list2:
            if q in number:
                number1.append(q)
        if len(number1) ==1:
            score+=5
            num+=1
        elif len(number1)>=2:
            score+=5
            num+=1
    #letter
        upper1 = []
        lower1 = []
        for k in password_list2:
            if k in upper1:
                upper1.append(k)
        if len(upper1)>=1:
            score+=5
            
        for u in password_list2:
            if u in lower:
                lower1.append(u)
        if len(lower1)>=1:
            score+=5
    #plus score
        if num==2:
            score+=2
        elif num==3:
            score+=3
        elif num==4:
            score+=5
    #reduce score

        for j in range(1,len(password_list2)):
            if password_list2[j]==password_list2[j-1]:
                score-=1
        if score>=40:
            return "very strong"
        elif  30<=score<40:
            return "strong"
        elif 20<=score<30:
            return "medium"
        elif 10<=score<=20:
            return "commonly"
        else:
            return "weak"

def choose():
    '''
    choose() is used to choose different functions:store/update,read all,remove all, retrieval,exit
    Parameter: nothing
    return:
    the number of your choice
    '''
    print("\n What do you want? \n")
    print("1. store/update new account(s) and password(s) \n2. read all account(s)/password(s) from local or cloud database \n3. remove all account(s)/password(s) from local or cloud database \n4. retrieval password from local database \n5. Exit \n")
    f = input("Please Enter a number: ")
    return f


def store():
    '''
    store() is used to generate new accounts and passwords
    users can choose whether generating random passwords or not
    users can store many passwords at the same time, and store them in a dictionary
    Parameter: nothing
    return:nothing
    output:
    password and password strength
    '''
    password =''
    while True:
        e = input("\nPlease enter the amounts of accounts and passwords you want to store/update: ")
        int_list = []
        sum1 = 0
        numstring_list = [str(i) for i in range(10)]
        int_list.extend(''.join(e))
        for i in int_list:
            if i in numstring_list:
                sum1+=1
        if sum1 ==len(int_list):
            e = int(e)
            break
        else:
            print("\nError!Please enter a number.\n")
            
          
                
        
                  
            
    for i in range(e):
        account = input("\nEnter the {}th  account :".format(i+1))
        accounts.append(account)
        while True:
            check = input("\n Do you want to generate random password? y/n:")
            if check =="y":
                password = random_password()
                passes.append(password)
                break

            elif check =="n":
                password = input("Please enter your password:")
                passes.append(password)
                break
            else:
                
                print("\n Error, please enter y or n")

                    
        #Check password strength
        level = analysis(password)
        print("\n",password)
        print("\n password Strength: ",level)
        passwords[account] = password


def management():
    '''
    management() is used to relogin, the functions of read, remove, retrieval cannot be used if users don't regin
    users should log in again
    if the account is old, users can use the functions of read, remove, retrieval
    if the account is new, the local data will be cleaned up
    Parameter: nothing
    return: nothing
    '''
    account = input("Please enter the account name of the password management system:")
    F = open("master.txt","a")
    F.close()
    with open("master.txt","r+") as K:
        master_list = K.readlines()
      
        account_list = []

        for i in master_list:
            n = i.find(":")
            ac = i[:n]
            account_list.append(ac)
            

        if account in account_list:
            for j in range(3):
                master = getpass.getpass("Please enter your Master Passcord for Project Password Manager:")
        
                if ("{}:{}\n".format(account,master) in master_list):
                    break
                else:
                    print("Error!")
                    
        else:
            while True:
                re_choice = input(("The old local database will be clean up, are you should you want to relogin?y/n "))
                if re_choice =="y":
                    update = open("local_database.txt", "w", encoding="utf-8")
                    update.close()
                    master = getpass.getpass("Please set a Master Passcord for Project Password Manager:")
                    K.write("{}:{}\n".format(account,master))
                    break
                elif re_choice =="n":
                    main()
                    break
                else:
                    print("\nError!Please type y or n")
                    
                
                    
                
      
    ##Check master passcode strength
    master_level = analysis(master)
    print("\n master passcode strength: ",master_level,"\n",end=" ")


   
    while True:
        f = choose()
    # Exit
        if f == "5":
            print("Finished\n")
            main()
            break
    # Store/update    
        elif f =="1":
            store()
            add = ""
            while add =="y" or "n":
                add = input("\n Do you want to add more accounts and passwords? y/n :")
                if add =="y":
                    store()
                elif add == "n":
                    print("\nFinished\n")
                    break
                else:
                    print("\n Error, please enter y or n")
                    
            ok = ""
            while True:
                #Store in Local or in Cloud?
                store1 = input("Do you want to store your account and password in local or in cloud?:y/n ")
                if store1 =="y":
                    choice = ""
                    while True:
                        choice = input("local or cloud?")
                        print(choice)
                        #Write to Cloud File
                    
                        if choice =="cloud":
                            print("\n You must install The Google Library to store in Cloud.")
                            print("\n To do so please install pip then enter: ")
                            print("\n pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
                            print("\n For more information please go to: ")
                            print("\n https://developers.google.com/sheets/api/quickstart/python")
                            print("\n")
                        
                            from googleapiclient.discovery import build
                            from google.oauth2 import service_account

                            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
                            SERVICE_ACCOUNT_FILE = 'keys.json'

                            creds = None
                            creds = service_account.Credentials.from_service_account_file(
                                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

                            # The ID of spreadsheet.
                            SAMPLE_SPREADSHEET_ID = '19EytQO6ze-ufRNpyE5N5IEDbQ6MMST8f2Ap0jr7n8qQ'

                            service = build('sheets', 'v4', credentials=creds)

                            # Call the Sheets API
                            sheet = service.spreadsheets()

                            usernames = [accounts]

                            resource1 = {
                            "majorDimension": "ROWS",
                            "values": usernames
                            }

                            range1 = "A2:A";
                            service.spreadsheets().values().append(
                            spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=range1,
                            body=resource1,
                            valueInputOption="USER_ENTERED"
                            ).execute()

                            past = [passes]

                            resource2 = {
                            "majorDimension": "ROWS",
                            "values": past
                            }

                            range2 = "B2:B";
                            service.spreadsheets().values().append(
                            spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=range2,
                            body=resource2,
                            valueInputOption="USER_ENTERED"
                            ).execute()
                            print("Written Successful")
                            break
                        
                    
                        #Write to Local File
                        elif choice =="local":
                            
                        #Open Database
                            password_list = []
                            for i in passwords:
                                password_list.append("{}:{}\n".format(i,passwords[i]))
                            pwd = open("local_database.txt", "a", encoding="utf-8")

                                
                            pwd.writelines(password_list)
                            pwd.close()
                            print("Written Successful")
                            print("\nFinished\n")
                            break
                        
                            
                        else:
                            print("Error, please enter cloud or local")
                    break
                
                if store1 =="n":
                    break
                else:
                    print("Error, please enter y or n")
            
                    
                            
                    
                    
                
        elif f =="2":
        #Verification
            
     
            while True:
                verify = getpass.getpass("Please enter your master passcode to enter: ")
                if verify != master:
                    print("Error!\ntry again")
                  
            
                else:
                    while True:
                        choice2 = input("You want to read all of your account(s) and password(s) from local or in cloud? :local/cloud ")

                        if choice2 == "local":
                            F = open("master.txt","a")
                            F.close()
                            pwd = open("local_database.txt", "r", encoding="utf-8")
                            answer = pwd.read()
                            pwd.close()
                            print(answer)
                            break
                        elif choice2 =="cloud":
                            print("\n You must install The Google Library to store in Cloud.")
                            print("\n To do so please install pip then enter: ")
                            print("\n pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
                            print("\n For more information please go to: ")
                            print("\n https://developers.google.com/sheets/api/quickstart/python")
                            print("\n")
                    
                            from googleapiclient.discovery import build
                            from google.oauth2 import service_account

                            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
                            SERVICE_ACCOUNT_FILE = 'keys.json'

                            creds = None
                            creds = service_account.Credentials.from_service_account_file(
                                    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

                            # The ID of spreadsheet.
                            SAMPLE_SPREADSHEET_ID = '19EytQO6ze-ufRNpyE5N5IEDbQ6MMST8f2Ap0jr7n8qQ'

                            service = build('sheets', 'v4', credentials=creds)

                            # Call the Sheets API
                            sheet = service.spreadsheets()
                            result1 = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                        range="A2:A").execute()
                            result2 = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                        range="B2:B").execute()
                            values1 = result1.get('values', [])
                            values2 = result2.get('values', [])

                            #Verification variable
                            verify = getpass.getpass("Please enter your master passcode to enter: ")

                            #Verification
                            while True:
                                if verify != master:
                                    verifying_again = getpass.getpass("\n Invalid Passcode, please try again: ")
                                    if verifying_again == master:
                                        print("\n Master Passcode Correct! Now Logined in: ")
                                        #print accounts and passwords
                                        print("Accounts: ",values1)
                                        print("Passwords: ",values2)
                                        break
                                else:
                                    print("\n Master Passcode Correct! Now Logined in: ")
                                    #print accounts and passwords
                                    print("Accounts: ",values1)
                                    print("Passwords: ",values2)
                                    break

                            print("\n Print successful")
                            print("\n")
                            break
                
                    break


        elif f =="3":

            #Verification
            while True:
                verify = getpass.getpass("Please enter your master passcode to enter: ")
                
                if verify != master:
                    print("\n Error!\ntry again ")

                        
                else:
                    while True:
                        print("\n Master Passcode Correct! Now Logined in: ")
                        #print accounts and passwords
                        print("\n Please select a file type to motify: ")
                        print("\n a. local database, b. cloud database")
                    
                        select = input("\n Please enter: ")
                        if select == "a":
                            pwd = open('local_database.txt', 'w', encoding='utf-8')

                            while True:
                                confirm = input("Are you sure that you want to delete all content in Local database? y/n : ")
                                if confirm == "y":
                                    pwd.truncate(0)
                                    pwd.close()
                                    print("\n Remove Successful")
                                    break
                                elif confirm == "n":
                                    print("\n Cancelled")
                                    break
                                else:
                                    print("\n Error, please enter y or n")
                            
                            break
                      
                          
                        if select =="b":
                            while True:
                                confirm = input("Are you sure that you want to delete all content in Cloud database? y/n : ")
                                if confirm == "y":
                                    from googleapiclient.discovery import build
                                    from google.oauth2 import service_account
                                    from pprint import pprint

                                    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
                                    SERVICE_ACCOUNT_FILE = 'keys.json'

                                    creds = None
                                    creds = service_account.Credentials.from_service_account_file(
                                            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

                                    # The ID of spreadsheet.
                                    SAMPLE_SPREADSHEET_ID = '19EytQO6ze-ufRNpyE5N5IEDbQ6MMST8f2Ap0jr7n8qQ'

                                    service = build('sheets', 'v4', credentials=creds)

                                    # Clear all values
                                    range_ = "A2:B"
                                    request = service.spreadsheets().values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_)
                                    response = request.execute()
                                    pprint(response)
                                    print("\n Remove Successful")
                                    break
                                elif confirm == "n":
                                    print("\n Cancelled")
                                    break
                        
                        
                                else:
                                    print("\n Error, please enter y or n")
                            
                       
                            break 
                        else:
                            print("\nError, pleasr enter a or b")
                    break
        elif f =="4":
            while True:
                choice3 = input("\nDo you save your password(s) in the local?y/n ")
                if choice3 =="n":
                    print("\nPlease deposit in local firstly\n")
                    
                    
                    break
                elif choice3 =="y":
                    File = open('local_database.txt', 'r', encoding='utf-8')
                    password_list2 = File.readlines()
                    File.close()
                    temp_dict = {}
                    for i in password_list2:
                        string = i[:-1]
                        lst = string.split(":")
                        temp_dict[lst[0]] = lst[-1]
                        

                   
                    choice4 = input("\nWhich account's password do you want to extract?")
                    if choice4 in temp_dict:
                        print("This password is:{}".format(temp_dict[choice4]))
                        break
                    else:
                        print("Sorry, this account doesn't exist.")
                        break


def update():
    '''
    update() is used to store/update password(s) without reloginning
    Parameter: nothing
    return: nothing
    '''
    while True:
        print("\n What do you want? \n")
        print("1. store/update new account(s) and password(s) \n2. Exit \n")
        f = input("Please Enter a number: ")
        if f == "2":
            print("Finished\n")
            main()
           
            break
    # Store/update    
        elif f =="1":
            store()
            add = ""
            while add =="y" or "n":
                add = input("\n Do you want to add more account(s) and password(s)? y/n :")
                if add =="y":
                    store()
                elif add == "n":
                    print("\nFinished\n")
                    break
                else:
                    print("\n Error, please enter y or n")
                    
            ok = ""
            while True:
                #Store in Local or in Cloud?
                store1 = input("Do you want to store your account(s) and password(s) in local or in cloud?:y/n ")
                if store1 =="y":
                    choice = ""
                    while True:
                        choice = input("local or cloud?")
                        print(choice)
                        #Write to Cloud File
                    
                        if choice =="cloud":
                            print("\n You must install The Google Library to store in Cloud.")
                            print("\n To do so please install pip then enter: ")
                            print("\n pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
                            print("\n For more information please go to: ")
                            print("\n https://developers.google.com/sheets/api/quickstart/python")
                            print("\n")
                        
                            from googleapiclient.discovery import build
                            from google.oauth2 import service_account

                            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
                            SERVICE_ACCOUNT_FILE = 'keys.json'

                            creds = None
                            creds = service_account.Credentials.from_service_account_file(
                                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

                            # The ID of spreadsheet.
                            SAMPLE_SPREADSHEET_ID = '19EytQO6ze-ufRNpyE5N5IEDbQ6MMST8f2Ap0jr7n8qQ'

                            service = build('sheets', 'v4', credentials=creds)

                            # Call the Sheets API
                            sheet = service.spreadsheets()

                            usernames = [accounts]

                            resource1 = {
                            "majorDimension": "ROWS",
                            "values": usernames
                            }

                            range1 = "A2:A";
                            service.spreadsheets().values().append(
                            spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=range1,
                            body=resource1,
                            valueInputOption="USER_ENTERED"
                            ).execute()

                            past = [passes]

                            resource2 = {
                            "majorDimension": "ROWS",
                            "values": past
                            }

                            range2 = "B2:B";
                            service.spreadsheets().values().append(
                            spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=range2,
                            body=resource2,
                            valueInputOption="USER_ENTERED"
                            ).execute()
                            print("Written Successful")
                            break
                        
                    
                        #Write to Local File
                        elif choice =="local":
                            
                        #Open Database
                            password_list = []
                            for i in passwords:
                                password_list.append("{}:{}\n".format(i,passwords[i]))
                            pwd = open("local_database.txt", "a", encoding="utf-8")

                                
                            pwd.writelines(password_list)
                            pwd.close()
                            print("Written Successful")
                            print("\nFinished\n")
                            break
                        
                            
                        else:
                            print("Error, please enter cloud or local")
                    break
                
                if store1 =="n":
                    break
                
                else:
                    print("Error, please enter y or n")
##main
def main():
    '''
    main() is used to call command helpers
    Parameter: nothing
    return: nothing
    
    '''
    while True:
        print("command helpers: \n a. enter the registering page\n b. store/update account(s) and password(s)")
        main_choice = input("\nPlease type a or b: ")
        if main_choice == "a":
            management()
            break
        if main_choice =="b":
            update()
            break
        else:
            print("\nError!Please type a or b.")
            
main()
           
        
        
        
        


                        
                    
                
                    
                    
                
            
                
                        

        
        
        
        
        
                
    
    
     
        
                
                
            
            
