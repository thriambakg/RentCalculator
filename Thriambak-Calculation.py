import cgitb
cgitb.enable()
example1_data = open(r"C:/Users/giriprtr/Desktop/Website/yuh.txt", "r")  # use \\ when writing the path of the file
lines = example1_data.readlines()  # get a list of all lines in the text file
# read the whole file line by line
for i in range(0, len(lines)):
     print(lines[i])
example1_data.close()  # close the file
