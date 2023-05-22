#get the namedtuple thing that he uses below 
from collections import namedtuple

#gets and integer; more complicated (perhaps unnecessarily so) than our own int_input
def get_int(prompt, lo=None, hi=None):
    while True:
        try:
            val = int(input(prompt))
            if (lo is None or lo <= val) and (hi is None or val <= hi):
                return val
        except ValueError:   # input string could not be converted to int
            pass

#takes 'options' as a parameter
def do_menu(options):
    print("\nWhich do you want to do?")
    #for each number, and option in the iterable 'options,' starting at 1...
    for num,option in enumerate(options, 1):
        #print the number that enumerate() is on, then a colon, then the option (why 'option.label'?)
        print("{num}: {label}".format(num=num, label=option.label))
    #creates a formatted string called prompt that asks the user for a choice
    prompt = "Please enter the number of your choice (1-{max}): ".format(max=len(options))
    #runs get_int() using the above prompt, subtracts 1 to account for how computers count
    choice = get_int(prompt, 1, len(options)) - 1
    #call the requested function on the user's choice
    options[choice].fn()    # call the requested function

def kick_goat():
    print("\nBAM! The goat didn't like that.")

def kiss_duck():
    print("\nOOH! The duck liked that a lot!")

def call_moose():
    print("\nYour trombone sounds rusty.")

#creates a namedtuple with an option assigned to both a label and a function(?)
Option = namedtuple("Option", ["label", "fn"])
options = [
    Option("Kick a goat", kick_goat),
    Option("Kiss a duck", kiss_duck),
    Option("Call a moose", call_moose)
]

#create a function
def main():
    #get the user's desired number of iterations
    num = get_int("Please enter the number of iterations: ")
    #run the do_menu() as many times as the user said they want it run
    for i in range(num):
        do_menu(options)

#dude idk
if __name__=="__main__":
    main()
