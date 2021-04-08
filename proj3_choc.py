#################################
##### Name: YuHua
##### Uniqname: simonhua
#################################

import sqlite3

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from a database called choc.db
DBNAME = 'choc.sqlite'
conn = sqlite3.connect(DBNAME)

# Part 1: Implement logic to process user commands
def process_command(command):
    
    query = command.splite(' ')
    if len(query) != 0:
        high_level = decideHighLevelCommands(query[0])
        if not high_level:
            print("Please check your input!")
            return False
        if high_level == 1:
            pass
        elif high_level == 2:
            pass
        elif high_level == 3:
            pass
        else:
            pass

    return []
def bars(option_commands):
    query = '''
    SELECT Bars.SpecificBeanBarName, Bars.Company, 
    '''
    if (len(option_commands) == 0):
def decideHighLevelCommands(opeartion):
    if (opeartion == 'bars'):
        return 1
    elif (opeartion == 'companies'):
        return 2
    elif (opeartion == 'countries'):
        return 3
    elif (opeartion == 'regions'):
        return 3
    else:
        return 0

def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 2 & 3: Implement interactive prompt and plotting. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print(help_text)
            continue

# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    interactive_prompt()
