import cgitb
cgitb.enable()

def signUppage():
     while True:
          file = open(r"C:/Users/giriprtr/Desktop/Website/yuh.txt", "w")
          firstname = input("First name: ")
          lastname = input("Last name: ")
          username = input("Username: ")
          password = input("Password: ")
          password2 = input("Repeat password: ")
          file.write(firstname + ', ')
          file.write(lastname + ', ')
          file.write(username + ', ')

          if (password == password2):
               file.write(password)
               break
          else:
               verify = input("Passwords do not match, Please enter the same password")
               if (verify == password):
                    file.write(password)
                    break


     file.close()

signUppage()