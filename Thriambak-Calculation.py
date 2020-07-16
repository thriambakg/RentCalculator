import cgitb
cgitb.enable()
import os.path

def signUppage():
     while True:
          firstname = input("First name: ")
          lastname = input("Last name: ")
          username = input("Username: ")
          password = input("Password: ")
          password2 = input("Repeat password: ")
          if (password == password2):
               file = open(username+','+password+".txt", "w")
               file.write(firstname + ', ')
               file.write(lastname + ', ')

               file.close()
               break
          else:
               pass


def loginpage():
     username = input('Username: ')
     password = input('password: ')
     access = os.path.isfile('C:/Users/giriprtr/PycharmProjects/RentCalculator/'+ username+','+password+'.txt')
     if access == True:
          print('yay')
     else:
          print('fail')








loginpage()