import cgitb
cgitb.enable()

def signUppage():
     while True:
          firstname = input("First name: ")
          lastname = input("Last name: ")
          username = input("Username: ")
          password = input("Password: ")
          password2 = input("Repeat password: ")
          if (password == password2):
               file = open(firstname + lastname + ".txt", "w")
               file.write(firstname + ', ')
               file.write(lastname + ', ')
               file.write(username + ', ')
               file.write(password)
               file.close()
               break
          else:
               pass









signUppage()