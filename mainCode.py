# IMPORT MODULES
import time
import sys
import mysql.connector as sql
mycon = sql.connect(host="localhost",user="sachinrk",password="Rk@9728211958",database="fbi")

if mycon.is_connected == False:
    print("\nSORRY DATABASES ERROR FOUND!!!!!\n\n")
cursor = mycon.cursor()

# CREATE TABLE
createMainTable = "CREATE TABLE IF NOT EXISTS FBI_MAIN_SERVER(SR_NO INT NOT NULL UNIQUE AUTO_INCREMENT,USER_NAME CHAR(50) NOT NULL,FATHER_NAME CHAR(50) NOT NULL,AADHAR_NUMBER BIGINT NOT NULL UNIQUE,ACCOUNT_NUMBER BIGINT NOT NULL UNIQUE,PHONE_NUMBER BIGINT NOT NULL UNIQUE,BALANCE FLOAT NOT NULL,USER_ID VARCHAR(255) PRIMARY KEY,INTERNET_BANKING CHAR(20) DEFAULT 'NOT AVAILABLE',DEBIT_CARD_NUMBER BIGINT DEFAULT NULL,CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,ANY_LOAN CHAR(50) DEFAULT 'NO LOAN',COMPLAINTS INT DEFAULT 0);"
cursor.execute(createMainTable)

# create variable

welcomeText = "\nWELCOME TO FBI(FORBE'S BANK IO INDIA) BANK\n"

# we need data for verify the FBI MEMBERS
selectAllFBIMembers = "select MEMBER_NAME,MEMBER_ID,PASSWORD from FBI_MEMBERS_LIST;"
cursor.execute(selectAllFBIMembers)
dataAllFBIMembers = cursor.fetchall()

# we need data all the four selectors for further use in withdraw,deposit,update services
selectIdAccNum = "select USER_NAME,AADHAR_NUMBER,ACCOUNT_NUMBER,USER_ID from FBI_MAIN_SERVER;"
cursor.execute(selectIdAccNum)
dataIdAccNum = cursor.fetchall()


if len(dataIdAccNum) != 0:
    # [(USER_NAME,AADHAR_NUMBER,ACCOUNT_NUMBER,USER_ID),(USER_NAME,AADHAR_NUMBER,ACCOUNT_NUMBER,USER_ID)]
    accNumber = dataIdAccNum[(cursor.rowcount)-1][2] + 1
    userIdNumber = dataIdAccNum[(cursor.rowcount)-1][3]
    userIdNumber = int(userIdNumber.replace("@FBIuser", "")) + 1  # convert string into integer forcily
else:
    userIdNumber = 1000
    accNumber = 47430000000000

# taking maximum debit card number from debit card list than increment the debit card number for the next user
selectAllDebit = "select debit_card_number from FBI_MAIN_SERVER;"
cursor.execute(selectAllDebit)
dataAllDebit = cursor.fetchall()
debitCardNo = 4342000000000000  # default
debitCardList = [4342000000000000]
if len(dataAllDebit) != 0:        # always True
    for i in dataAllDebit:
        # print(type(i[0]))
        if i[0] != None:
            debitCardList.append(i[0])
debitCardNo = max(debitCardList)

# DEFINE FUNCTIONS

def welcome(str1):
    print("-"*167)
    print(str1)
    print("-"*167)

def animatedDots():
    for i in range(5):
        time.sleep(0.5)
        print(".",end="")
    print(".",end="")
    time.sleep(0.5)
    print(".")

def currentTimeUser(dataIdAccNum):
    selectIdAccNum = "select USER_NAME,AADHAR_NUMBER,ACCOUNT_NUMBER,USER_ID from FBI_MAIN_SERVER;"
    cursor.execute(selectIdAccNum)
    dataIdAccNum = cursor.fetchall()
    return dataIdAccNum

def findWithdrawUser(inputAccNo, inputAdhar, dataIdAccNum, isFbiUser):
    dataIdAccNum = currentTimeUser(dataIdAccNum)
    for i in dataIdAccNum:
        if (inputAccNo == i[2] and inputAdhar == i[1]):
            isFbiUser = True
            return i[0],i[3],isFbiUser        #(USER_NAME,AADHAR_NUMBER,ACCOUNT_NUMBER,USER_ID)

def findDepositUser(inputAccNo, dataIdAccNum, isFbiUser):
    dataIdAccNum = currentTimeUser(dataIdAccNum)
    for i in dataIdAccNum:
        if (inputAccNo == i[2]):
            isFbiUser = True
            return i[0],i[3],isFbiUser        #(USER_NAME,AADHAR_NUMBER,ACCOUNT_NUMBER,USER_ID)

def findUserId(inputAccNo, inputAdhar, dataIdAccNum, isFbiUser):
    dataIdAccNum = currentTimeUser(dataIdAccNum)
    for i in dataIdAccNum:
        if (inputAccNo == i[2] and inputAdhar == i[1]):
            isFbiUser = True
            return i[0], i[3], isFbiUser

def checkFBIMember(Id,pswrd,dataAllFBIMembers,isFBIMemeber):
    for i in dataAllFBIMembers:
        if (Id == i[1] and pswrd == i[2]):
            isFBIMemeber = True
            return i[0],isFBIMemeber

def loginFBIMembers():
    Id = input("\nENTER YOUR ID => ")
    pswrd = input("\nENTER YOUR PASSWORD => ")
    isFBIMemeber = False
    print("\nPROCESSING",end="")
    animatedDots()
    print("-"*167)
    try:
        fbiMember,isFBIMemeber = checkFBIMember(Id,pswrd,dataAllFBIMembers,isFBIMemeber)
    except:
        sys.stderr.write("\nMEMBER NOT FOUND\n")
        return 

    if isFBIMemeber==True:
        print("-"*167)
        print("\nwelcome {}\n".format(fbiMember))
        print("-"*167)
        
        while True:
            print("\nPRESS 1: SHOW ALL USERS")
            print("PRESS 2: SHOW THE USERS HAVING BALANCE GREATER THAN :")
            print("PRESS 3: SHOW THE USERS HAVE APPLY FOR LOAN")
            print("PRESS 4: FOR MISCELLANEOUS SEARCH")
            print("PRESS 5: FOR EXIT")
            write = input("\nENTER CHOICE FROM ABOVE : ").upper()
            if write=="1":
                try:
                    cursor.execute("SELECT * FROM FBI_MAIN_SERVER;")
                except:
                    sys.stderr.write("\nDATA NOT FOUND ERROR\n")
                    time.sleep(1.5)
                dataFor1 = cursor.fetchall()
                print("\nCOLLECTING DATA",end="")
                animatedDots()
                print("-"*167)
                for i in dataFor1:
                    print(i)
                print("-"*167)
            
            elif write=="2":
                try:
                    cursor.execute("SELECT * FROM FBI_MAIN_SERVER where balance>{};".format(int(input("\nENTER AMOUNT : "))))
                except:
                    sys.stderr.write("\nDATA NOT FOUND ERROR\n")
                    time.sleep(1.5)
                dataFor2 = cursor.fetchall()
                print("\nCOLLECTING DATA",end="")
                animatedDots()
                print("-"*167)
                for i in dataFor2:
                    print(i)
                print("-"*167)

            elif write=="3":
                try:
                    cursor.execute("SELECT * FROM FBI_MAIN_SERVER where ANY_LOAN!='NO LOAN';")
                except:
                    sys.stderr.write("\nDATA NOT FOUND ERROR\n")
                    time.sleep(1.5)
                dataFor3 = cursor.fetchall()
                print("\nCOLLECTING DATA",end="")
                animatedDots()
                print("-"*167)
                if len(dataFor3)==0:
                    print("\nEMPTY ROW")
                for i in dataFor3:
                    print(i)
                print("-"*167)
            elif write=="4":
                sqlQuery = input("\nWRITE SQL QUERY HERE : ").upper()
                try:
                    cursor.execute(sqlQuery)
                except:
                    sys.stderr.write("\nSQL SYNTAX ERROR\n")
                    time.sleep(1.5)
                if ("UPDATE" in sqlQuery or "ALTER" in sqlQuery):
                    mycon.commit()
                dataFor4 = cursor.fetchall()
                print("\nCOLLECTING DATA",end="")
                animatedDots()
                print("-"*167)
                for i in dataFor4:
                    print(i)
                print("-"*167)
            elif (write=="5"):
                return "\nEXIT..."
            else:
                sys.stderr.write("\nINVALID KEY!! PRESS AGAIN\n")
                time.sleep(2)
    else:
        sys.stderr.write("\nMEMBER NOT FOUND\n")
        return

def openAccount(userIdNumber, accNumber):
    name = input("\nENTER YOUR FULL NAME:  ").upper()
    father = input("\nENTER FATHERS NAME:  ").upper()
    aadhar = int(input("\nENTER YOUR AADHAR:  "))
    phNumber = int(input("\nENTER YOUR PHONE NUMBER:  "))
    userid = "@FBIuser" + str(userIdNumber)
    firstDeposit = int(input("ENTER FIRST DEPOSIT MONEY : "))

    # INSERT VALUES
    insertData = "insert into FBI_MAIN_SERVER(USER_NAME,FATHER_NAME,AADHAR_NUMBER,ACCOUNT_NUMBER,PHONE_NUMBER,BALANCE,USER_ID) values ('{}','{}',{},{},{},{},'{}')".format(
        name, father, aadhar, accNumber, phNumber, firstDeposit, userid)
    cursor.execute(insertData)
    mycon.commit()
    print("\nCREATING YOUR ACCOUNT ",end="")
    animatedDots()
    sys.stderr.write("\nNOTE YOUR ACCOUNT NUMBER : {}".format(accNumber))
    print("\nACCOUNT CREATED SUCCESFULLY\n")
    userIdNumber += 1
    accNumber += 1
    return userIdNumber,accNumber

def withdrawMoney(dataIdAccNum):
    inputAccNo = int(input("\nENTER YOUR ACCOUNT NUMBER => "))
    inputAadhar = int(input("\nENTER YOUR AADHAR NUMBER => "))
    # use of sleep function here
    print("\nCHECKING YOU ARE FBI USER OR NOT !!!")
    print("\nPROCESSING",end="")
    animatedDots()
    isFbiUser = False
    try:        #if any error than execute the except block       
        fbiUserName,userId,isFbiUser = (findWithdrawUser(inputAccNo, inputAadhar, dataIdAccNum, isFbiUser))
    except:
        sys.stderr.write("\n USER NOT FOUND\n")
        return 
    if isFbiUser == True:
        print("-"*167)
        print("\nwelcome {}\n".format(fbiUserName))
        print("-"*167)
        returnMoney = int(input("\nENTER MONEY YOU WANT WITHDRAW : "))
        sure = input("\nwrite \"OK\" for confirmation otherwise transaction cancel : ").upper()
        if sure == "OK":
            cursor.execute("update FBI_MAIN_SERVER set balance=balance-{} where ACCOUNT_NUMBER={};".format(returnMoney, inputAccNo))
            mycon.commit()
            createUserHistory = "CREATE TABLE IF NOT EXISTS {}(SR_NO INT NOT NULL UNIQUE AUTO_INCREMENT,ACCOUNT_NUMBER BIGINT,AMOUNT_WITHDRAW FLOAT DEFAULT NULL,AMOUNT_DEPOSIT FLOAT DEFAULT NULL,TRANSACTION_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP);".format(userId.replace("@","AT"))
            cursor.execute(createUserHistory)
            insertHistory = "INSERT INTO {} (ACCOUNT_NUMBER,AMOUNT_WITHDRAW) VALUES({},{});".format(userId.replace("@","AT"), inputAccNo, returnMoney)
            cursor.execute(insertHistory)
            mycon.commit()
            print("\nPROCESSING",end="")
            animatedDots()
            print("-"*167)
            print("\nPAYMENT SUCCESFULLY DONE")
            return 
        else:
            sys.stderr.write("\nTRANSACTION CANCELED\n")
            return
    else:
        sys.stderr.write("\n USER NOT FOUND\n")
        return

def depositMoney():
    inputAccNo = int(input("\nENTER YOUR ACCOUNT NUMBER => "))
    # use sleep function here
    print("CHECKING YOU ARE FBI USER OR NOT !!!")
    print("\nPROCESSING",end="")
    animatedDots()
    isFbiUser = False
    try:
        fbiUserName,userId,isFbiUser = (findDepositUser(inputAccNo, dataIdAccNum, isFbiUser))
    except:
        sys.stderr.write("\nUSER NOT FOUND\n")
        return
    if isFbiUser == True:
        print("-"*167)
        print("\nwelcome {}\n".format(fbiUserName))
        print("-"*167)
        money = int(input("\nENTER MONEY YOU WANT DEPOSIT => "))
        cursor.execute("update FBI_MAIN_SERVER set balance=balance+{} where ACCOUNT_NUMBER={};".format(money, inputAccNo))
        mycon.commit()
        # create table with table name is user name for record  transaction histry
        createUserHistory = "CREATE TABLE IF NOT EXISTS {}(SR_NO INT NOT NULL UNIQUE AUTO_INCREMENT,ACCOUNT_NUMBER BIGINT,AMOUNT_WITHDRAW FLOAT DEFAULT NULL,AMOUNT_DEPOSIT FLOAT DEFAULT NULL,TRANSACTION_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP);".format(userId.replace("@","AT"))
        cursor.execute(createUserHistory)
        insertHistory = "INSERT INTO {} (ACCOUNT_NUMBER,AMOUNT_DEPOSIT) VALUES({},{});".format(userId.replace("@","AT"), inputAccNo, money)
        cursor.execute(insertHistory)
        mycon.commit()
        print("\nTRANSFERrING AMOUNT",end="")
        animatedDots()
        print("\nDEPOSIT  SUCCESFULLY DONE")
        return 

    else:
        sys.stderr.write("\nUSER NOT FOUND\n")
        return

def checkBalance():
    inputAccNo = int(input("\nENTER YOUR ACCOUNT NUMBER => "))
    inputAadhar = int(input("\nENTER YOUR AADHAR NUMBER => "))
    # use of sleep function here
    print("\nPROCESSING",end="")
    animatedDots()
    print("-"*167)
    isFbiUser = False
    try:
        fbiUserName, userId, isFbiUser = (findWithdrawUser(inputAccNo, inputAadhar, dataIdAccNum, isFbiUser))
    except:
        sys.stderr.write("\nUSER NOT FOUND\n")
        return
    if isFbiUser == True:
        print("-"*167)
        print("\nwelcome {}\n".format(fbiUserName))
        print("-"*167)
        cursor.execute("select balance from FBI_MAIN_SERVER where account_number={};".format(inputAccNo))
        balanceList = cursor.fetchall()
        print("PROCESSING")
        animatedDots()
        print("\nYOUR BALANCE IS => ", balanceList[len(balanceList)-1][0])
    else:
        sys.stderr.write("\n USER NOT FOUND\n")
        return

def transactionHistory():
    inputAccNo = int(input("\nENTER YOUR ACCOUNT NUMBER => "))
    # use of sleep function here
    print("\nPROCESSING",end="")
    animatedDots()
    print("-"*167)
    isFbiUser = False
    try:
        fbiUserName, userId, isFbiUser = (findDepositUser(inputAccNo, dataIdAccNum, isFbiUser))
    except:
        sys.stderr.write("\n USER NOT FOUND\n")
        return
    if isFbiUser == True:
        print("-"*167)
        print("\nwelcome {}\n".format(fbiUserName))
        print("-"*167)
        selectHistory = "select * from {}".format(userId.replace("@","AT"))
        try:        #ERROR THAN RUN EXCEPT BLOCK
            cursor.execute(selectHistory)
        except:
            sys.stderr.write("\n NO TRANSACTION HAVE BEEN YET\n")
            return
        dataHistory = cursor.fetchall()
        print("COLLECTING DATA")
        animatedDots()
        print("SR NO.", "WITHDRAW MONEY", "DEPOSIT MONEY","TRANSACTION TIME", sep="  ")
        if len(dataHistory)==0:
            print("\nNO TRANSACTION HAVE BEEN YET")
        for i in dataHistory:
            print(" ", i[0], "\t  ", i[2], "\t", i[3], "\t\t", i[4])
        return " "
    else:
        sys.stderr.write("\n USER NOT FOUND\n")
        return

def applyServices(dataIdAccNum):
    print("\n APPLY FOR FBI ONLINE SERVICES.\n")
    inputAccNo = int(input("\nENTER YOUR ACCOUNT NUMBER => "))
    inputAadhar = int(input("\nENTER YOUR AADHAR NUMBER => "))
    isFbiUser = False
    print("\nCHECKING YOU ARE FBI USER OR NOT")
    print("\nPROCESSING",end="")
    animatedDots()
    print("-"*167)
    try:
        fbiUserName, userId, isFbiUser = findUserId(inputAccNo, inputAadhar, dataIdAccNum, isFbiUser)
    except:
        sys.stderr.write("\n USER NOT FOUND\n")
        return
    if isFbiUser == True:
        print("-"*167)
        print("\nwelcome {}\n".format(fbiUserName))
        print("-"*167)
        print("\nPRESS 1: APPLY FOR DEBIT CARD REQUEST")
        print("PRESS 2: REGISTER TO INTERNET BANKING")
        print("PRESS 3: APPLY FOR HOME LOAN")
        print("PRESS 4: APPLY FOR HEALTH LOAN")
        print("PRESS \"5\" OR \"x\" FOR EXIT")
        press = input("\nENTER THE KEY :\t").upper()
        if (press == "1"):
            cursor.execute("select debit_card_number from fbi_main_server where user_id='{}';".format(userId))
            data1 = cursor.fetchall()
            if (data1[0][0]!=None):
                time.sleep(1)
                print("\n DEBIT CARD IS ALREADY ISSUED..")
                return "\n IF YOU HAVE LOST DEBIT CARD THAN INFORM THE YOUR BASE BANK BRANCH AND APLPY FOR NEW ONE"
            addDebitNo = "update FBI_MAIN_SERVER set debit_card_number={} where account_number={};".format(debitCardNo+1, inputAccNo)
            cursor.execute(addDebitNo)
            mycon.commit()
            print("\nPROCESSING",end="")
            animatedDots()
            print("-"*167)
            print("\nYOUR DEBIT CARD NO : {}\nPLEASE COLLECT FROM YOUR BASE BRANCH".format(debitCardNo+1))
            return
        elif (press == "2"):
            addInternetBanking = "update FBI_MAIN_SERVER set internet_banking='AVAILABLE' where account_number={};".format(
                inputAccNo)
            cursor.execute(addInternetBanking)
            mycon.commit()
            print("\nPROCESSING",end="")
            animatedDots()
            print("-"*167)
            print("\nNOW INTERNET BANKING IS AVAILABLE FOR YOU\nYOUR USERID : '{}'\nCOLLECT OR RESET PASSWORD FROM YOUR BASE BANK BRANCH".format(userId))
            return
        elif (press == "3"):
            selectLoans = "select any_loan from FBI_MAIN_SERVER where account_number={};".format(
                inputAccNo)
            cursor.execute(selectLoans)
            dataLoanList1 = cursor.fetchall()
            strfrmt1 = dataLoanList1[0][0]
            if (strfrmt1 == "NO LOAN" or strfrmt1 == "no loan"):
                strfrmt1 = "HOME LOAN"
            else:
                strfrmt1 = strfrmt1 + ",HOME LOAN"
            addLoan = "update FBI_MAIN_SERVER set any_loan='{}' where account_number={};".format(
                strfrmt1, inputAccNo)
            cursor.execute(addLoan)
            mycon.commit()
            print("\nPROCESSSING.........")

            print("-"*167)
            time.sleep(3)
            print("\nSUCCESFULLY APPLIED FOR HOME LOAN\nPLEASE COLLECT AMOUNT OF YOUR LOAN FROM BASE BRANCH")
            return

        elif (press == "4"):
            selectLoans = "select any_loan from FBI_MAIN_SERVER where account_number={};".format(
                inputAccNo)
            cursor.execute(selectLoans)
            dataLoanList2 = cursor.fetchall()
            strfrmt2 = dataLoanList2[0][0]
            if (strfrmt2 == "NO LOAN" or strfrmt2 == "no loan"):
                strfrmt2 = "HEALTH LOAN"
            else:
                strfrmt2 = strfrmt2 + ",HEALTH LOAN"
            addLoan = "update FBI_MAIN_SERVER set any_loan='{}' where account_number={};".format(
                strfrmt2, inputAccNo)
            cursor.execute(addLoan)
            mycon.commit()
            print("\nPROCESSSING.........")

            print("-"*167)
            time.sleep(3)
            print("\nSUCCESFULLY APPLIED FOR HEALTH LOAN\nPLEASE COLLECT AMOUNT OF YOUR LOAN FROM BASE BRANCH")
            return

        elif (press == "X" or press == "5"):
            print("\n EXIT")
            return
        else:
            sys.stderr.write("\nINVALID KEY PRESS\nHENCE EXIT\n")
            return
    else:
        sys.stderr.write("\nUSER NOT FOUND\n")
        return

def updateDetails():
    print("\n You can only update your \"NAME\",\"FATHER NAME\",\"PHONE NUMBER\" only.\n")
    inputAccNo = int(input("\nENTER YOUR ACCOUNT NUMBER => "))
    inputAadhar = int(input("\nENTER YOUR AADHAR NUMBER => "))
    isFbiUser = False
    print("\nCHECKING YOU ARE FBI USER OR NOT")
    print("\nPROCESSING",end="")
    animatedDots()
    print("-"*167)
    try:
        fbiUserName,userId,isFbiUser = findWithdrawUser(inputAccNo, inputAadhar, dataIdAccNum, isFbiUser)
    except:
        return "\nUSER NOT FOUND"
    if isFbiUser == True:
        print("-"*167)
        print("\nwelcome {}\n".format(fbiUserName))
        print("-"*167)
        while True:
            print("PRESS 1: UPDATE NAME")
            print("PRESS 2: UPDATE FATHER NAME")
            print("PRESS 3: UPDATE PHONE NUMBER")
            print("PRESS 4 OR \"x\" FOR EXIT")
            press = input("\nENTER THE KEY :\t").upper()
            if (press == "1"):
                udtName = input("\nENTER YOUR UPDATED NAME => ").upper()
                updateQuery = "update FBI_MAIN_SERVER set user_name='{}' where account_number='{}';".format(
                    udtName, inputAccNo)
                cursor.execute(updateQuery)
                mycon.commit()  # DON'T FORGET TO WRITE <CONNECTOR-OBJECT>.COMMIT()
                print("\n UPDATING",end="")
                animatedDots()
                print("\nYOUR NAME UPDATED SUCCESFULLY")
                print("-"*167)

            elif (press == "2"):
                udtFatherName = input(
                    "\nENTER YOUR UPDATED FATHER NAME => ").upper()
                updateQuery = "update FBI_MAIN_SERVER set father_name='{}' where account_number='{}';".format(
                    udtFatherName, inputAccNo)
                cursor.execute(updateQuery)
                mycon.commit()  # DON'T FORGET TO WRITE <CONNECTOR-OBJECT>.COMMIT()
                print("\n UPDATING",end="")
                animatedDots()
                print("\nYOUR FATHER NAME UPDATED SUCCESFULLY")
                print("-"*167)

            elif (press == "3"):
                udtPhNo = input("\nENTER YOUR UPDATED PHONE NUMBER => ")
                updateQuery = "update FBI_MAIN_SERVER set phone_number={} where account_number='{}';".format(
                    udtPhNo, inputAccNo)
                cursor.execute(updateQuery)
                mycon.commit()  # DON'T FORGET TO WRITE <CONNECTOR-OBJECT>.COMMIT()
                print("\n UPDATING",end="")
                animatedDots()
                print("\n--------SUCCESSFULLY UPDATED --------\n")
                return
            elif (press == "X" or press == "4"):
                print("\n SUCCESFULLY UPDATED")
                return
            else:
                sys.stderr.write("\nINVALID KEY!!! PRESS AGAIN\n")

def feedback():
    inputName = input("\nENTER YOUR NAME => ").upper()
    inputGender = input("\nENTER YOUR GENDER (M/F) => ").upper()
    if inputGender == "":
        inputGender = "M"
    description = input(
        "\nGIVE YOUR FEEDBACKK (DON'T USE SPECIAL CHARACTERS) : ").capitalize()
    feedbackTable = "CREATE TABLE IF NOT EXISTS FEEDBACK(SR_NO INT NOT NULL UNIQUE AUTO_INCREMENT,USER_NAME CHAR(50) NOT NULL,GENDER CHAR(1) NOT NULL DEFAULT 'M',FEEDBACK_DESCRIPTION TEXT NOT NULL,FEEDBACK_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
    try:
        cursor.execute(feedbackTable)
    except:
        return "\nSOMETHING WENT WRONG"
    insertFeedback = "INSERT INTO FEEDBACK (USER_NAME,GENDER,FEEDBACK_DESCRIPTION) VALUES('{}','{}','{}');".format(
        inputName, inputGender, description)
    cursor.execute(insertFeedback)
    mycon.commit()
    return "\nWE WORK ON YOUR FEEDBACK\nTHANK YOU"

welcome(welcomeText)    # CALLING THE WELCOME FUNCTION

while True:
    print("\nPRESS *: LOGIN MEMEBERS OF FBI")
    print("PRESS 1: OPEN ACCOUNT")
    print("PRESS 2: WITHDRAW MONEY")
    print("PRESS 3: DEPOSIT MONEY")
    print("PRESS 4: CHECK BALANCE")
    print("PRESS 5: SHOW TRANSACTION HISORY")
    print("PRESS 6: APPLY FOR FBI SERVICES/FBI LOANS")
    print("PRESS 7: UPDATE USER DETAILS")
    print("PRESS 8: GIVE FEEDBACK")
    print("PRESS 9: EXIT")
    press = input("\nENTER THE KEY :\t")
    if (press == "*"):
        welcomeText = "\nLOGIN MEMEBERS OF FBI\n"
        welcome(welcomeText)    # CALLING THE WELCOME FUNCTION
        loginFBIMembers()
        print("-"*167)
        time.sleep(2)

    elif (press == "1"):
        welcomeText = "\nOPEN ACCOUNT\n"
        welcome(welcomeText)    # CALLING THE WELCOME FUNCTION
        userIdNumber,accNumber = openAccount(userIdNumber, accNumber)
        print("-"*167)
        time.sleep(3)

    elif (press == "2"):
        welcomeText = "\nWITHDRAW MONEY\n"
        welcome(welcomeText)    # CALLING THE WELCOME FUNCTION
        withdrawMoney(dataIdAccNum)
        print("-"*167)
        time.sleep(3)

    elif (press == "3"):
        welcomeText = "\nDEPOSIT MONEY\n"
        welcome(welcomeText)    # CALLING THE WELCOME FUNCTION
        depositMoney()
        print("-"*167)
        time.sleep(3)

    elif (press == "4"):
        welcomeText = "\nCHECK BALANCE\n"
        welcome(welcomeText)    # CALLING THE WELCOME FUNCTION
        checkBalance()
        print("-"*167)
        time.sleep(3)

    elif (press == "5"):
        welcomeText = "\nSHOW TRANSACTION HISTORY\n"
        welcome(welcomeText)    # CALLING THE WELCOME FUNCTION
        transactionHistory()
        print("-"*167)
        time.sleep(3)

    elif (press == "6"):
        welcomeText = "\nAPPLY FOR FBI SERVICES/FBI LOANS\n"
        welcome(welcomeText)    # CALLING THE WELCOME FUNCTION
        applyServices(dataIdAccNum)
        print("-"*167)
        time.sleep(3)

    elif (press == "7"):
        welcomeText = "\nUPDATE USER DETAILS\n"
        welcome(welcomeText)    # CALLING THE WELCOME FUNCTION
        updateDetails()
        print("-"*167)
        time.sleep(3)

    elif (press == "8"):
        welcomeText = "\nGIVE FEEDBACK\n"
        welcome(welcomeText)    # CALLING THE WELCOME FUNCTION
        print(feedback())
        print("-"*167)
        time.sleep(3)

    elif (press == "9"):
        # I may use sleep function in that case
        print("\nYOU PRESS \"9\"")
        print("\nEXIT!!!",end="")
        animatedDots()
        print("-"*167)
        break
    else:
        sys.stderr.write("-"*167)
        sys.stderr.write("\nINVALID KEY!! PRESS AGAIN\n")
        sys.stderr.write("-"*167)
        sys.stderr.write("\n")
        time.sleep(2)
