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
               file.write(password)
               break
          else:
               verify = input("Passwords do not match, Please enter the same password")
               if (verify == password):
                    file.write(password)
                    break
          file = open(firstname+lastname+".txt", "w")
          file.write(username + ', ')




     file.close()

signUppage()