#################################
##### Name: YuHua
##### Uniqname: simonhua
#################################

import sqlite3
import plotly.graph_objs as go

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from a database called choc.db
DBNAME = 'choc.sqlite'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()
# Part 1: Implement logic to process user commands

# Here is what parameters are acceptable for each type of command
# [none|country=<alpha2>| region=<name>], default=none is a little bit different
# then I seperate them from the others.
parameters_valid_part1 = [
    ['none', 'sell', 'source', 'ratings', 'cocoa', 'top', 'bottom'],
    ['none', 'ratings', 'cocoa', 'number_of_bars', 'top', 'bottom'],
    ['none', 'sell', 'source', 'ratings', 'cocoa', 'number_of_bars', 'top', 'bottom'],
    ['sell', 'source', 'ratings', 'cocoa', 'number_of_bars', 'top', 'bottom']
]
# Here is for [none|country=<alpha2>| region=<name>], default=none seperately
parameters_valid_part2 = [
    ['country=', 'region='],
    ['country=', 'region='],
    ['region='],
    [],
]

# Print the results in a specific format 
def print_result(command, high_level, tmp, output):
    # For bars and default=bars printing
    if high_level == 0 or high_level == 1:
        for list_data in output:
            tmp = list(list_data)
            for i in [0, 1, 2, 5]:

                # truncate values that are too long appropriately and add the ‘...’ at the end.
                if len(tmp[i]) > 12:
                    tmp[i] = tmp[i][:12] + '...'
            # printing records with fixed- width formatting.
            print('| {:^15} | {:^15} | {:^15} | {:^15.1f} | {:^15.0%} | {:^15} |'.format(tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5]))
    
    # For companies and countries printing
    elif high_level == 2 or high_level == 3:
        for list_data in output:
            tmp = list(list_data)
            for i in [0, 1]:

                # truncate values that are too long appropriately and add the ‘...’ at the end.
                if len(tmp[i]) > 12:
                    tmp[i] = tmp[i][:12] + '...'

            # set float data format
            if isinstance(tmp[2], float):
                tmp[2] = round(tmp[2], 1)

            # cocoaPercent needs to present like "70%"
            # printing records with fixed- width formatting.
            if 'cocoa' in command:
                print('| {:^15} | {:^15} | {:^15.0%} |'.format(tmp[0],tmp[1],tmp[2]))
            else:
                print('| {:^15} | {:^15} | {:^15} |'.format(tmp[0],tmp[1],tmp[2]))
    elif high_level == 4:
        for list_data in output:
            tmp = list(list_data)

            # truncate values that are too long appropriately and add the ‘...’ at the end.
            if len(tmp[0]) > 12:
                tmp[0] = tmp[0][:12] + '...'
            
            # set float data format
            if isinstance(tmp[1], float):
                tmp[1] = round(tmp[1], 1)

            # cocoaPercent needs to present like "70%"
            # printing records with fixed- width formatting.
            if 'cocoa' in command:
                print('| {:^15} | {:^15.0%} |'.format(tmp[0],tmp[1]))
            else:
                print('| {:^15} | {:^15} |'.format(tmp[0],tmp[1]))
    print('')

# The 'process_command'function takes a string and returns a list of tuples. The string 
# is a command that would be entered by a user (for example 'bars sell region=Europe 
# cocoa bottom 5). The return would be the records that match the query, including the 
# fields that are relevant to the type of command. There are four high-level commands, 
# each of which can take a set of options. Each option has a default value that must be 
# used if the option is omitted. 
def process_command(command):
    # I split the input command into a list of string
    query = command.split(' ')

    # If the input is nothing, then return []
    if len(query) != 0:
        # Determine which command the program needs to deal with(bars, companies, countries or regions)
        high_level = decideHighLevelCommands(query[0])

        # For bars and default=bars
        if high_level == 0 or high_level == 1:

            # If it is 'bars' then delete the first element, or using all the input
            if high_level == 1:
                query = query[1:]

            # call  the bars function
            output = bars(query)
            tmp = list(output)

            # Print the output 'nicely'
            if (len(output) != 0):
                print_result(query, high_level, tmp, output)

                # deal with the situation like:
                # "regions sell cocoa barplot"
                # Where the command line contains barplot already
                if 'barplot' in command:
                    barplot(command, output)

            return output

        # For companies
        elif high_level == 2:

            # call the companies function
            output = companyies(query[1:])
            tmp = list(output)

            # Print the output 'nicely'
            if (len(output) != 0):
                print_result(query[1:], high_level, tmp, output)
                
            # deal with the situation like:
            # "regions sell cocoa barplot"
            # Where the command line contains barplot already
            if 'barplot' in command:
                barplot(command, output)

            return output

        # For countries
        elif high_level == 3:

            # call the companies function
            output = countries(query[1:])
            tmp = list(output)

            # Print the output 'nicely'
            if (len(output) != 0):
                print_result(query[1:], high_level, tmp, output)
                
                # deal with the situation like:
                # "regions sell cocoa barplot"
                # Where the command line contains barplot already
                if 'barplot' in command:
                    barplot(command, output)

            return output
        
        # For regions
        else:
            # call the companies function
            output = regions(query[1:])
            tmp = list(output)

            # Print the output 'nicely'
            if (len(output) != 0):
                print_result(query[1:], high_level, tmp, output)

                # deal with the situation like:
                # "regions sell cocoa barplot"
                # Where the command line contains barplot already
                if 'barplot' in command:
                    barplot(command, output)

            return output
    return []

# Here is a function to determine which high level command 
# the program needs to deal with.
def decideHighLevelCommands(opeartion):
    # bars
    if (opeartion == 'bars'):
        return 1
    # companies
    elif (opeartion == 'companies'):
        return 2

    # countries
    elif (opeartion == 'countries'):
        return 3

    # regions
    elif (opeartion == 'regions'):
        return 4

    # default=bars 
    # the other invalid input will also return 0, whether the input is valid
    # will be checked below in the function 'checkvalidation'
    else:
        return 0

# Before the program implementing the commands, the program 
# will check whether the commands is valid.
def checkvalidatoin(option_commands, type):
    checklist = [
        [False, False, False, False, False, False],
        [False, False, False, False, False, False],
        [False, False, False, False, False, False],
        [False, False, False, False, False, False]
    ]
    for option in option_commands:
    
        # Check for part1 (defined at the beginning), <integer> or [barplot]
        if option in parameters_valid_part1[type] or option.isdigit() or option == 'barplot':
            
            # Check whether each parameter only input once
            if option == 'sell' or option == 'source':
                if checklist[type][1]:
                    print('- [sell|source], default=sell. You can only set one of them, Input again!')
                    print('')
                    return False
                else:
                    checklist[type][1] = True 
            elif option == 'ratings' or option == 'cocoa' or option == 'number_of_bars':
                if checklist[type][2]:
                    print('- [ratings|cocoa|number_of_bars], default=ratings.You can only set one of them, Input again!')
                    print('')
                    return False
                else:
                    checklist[type][2] = True
            elif option == 'top' or option == 'bottom':
                if checklist[type][3]:
                    print('- [top|bottom], default=top. You can only set one of them, Input again!')
                    print('')
                    return False
                else:
                    checklist[type][3] = True
            elif option.isdigit():
                if checklist[type][4]:
                    print('- <integer>, default=10. You can only input one integer, Input again!')
                    print('')
                    return False
                else:
                    checklist[type][4] = True
            elif option == 'barplot':
                if checklist[type][5]:
                    print("- [barplot]. You can only input one time 'barplot', Input again!")
                    print('')
                    return False
                else:
                    checklist[type][5] = True
            continue

        # Check for part2 (defined at the beginning)
        bFind = False
        for ele in parameters_valid_part2[type]:
            if ele in option:
                bFind = True
                break
        if (bFind):

            # Check whether each parameter only input once
            if checklist[type][0]:
                print("- [none|country=<alpha2>| region=<name>], default=none. You can only set one of them, Input again!")
                print('')
                return False
            else:
                checklist[type][0] = True
            continue

        # Check for " "
        if option == "":
            print('Please check your input, Extra space is invalid. Input again!')
            print('')
            return False

        # Output where is wrong
        print('Please check your input, "' + option +'" is invalid. Input again!')
        print('')
        return False
    return True

# This is a template for - [ratings|cocoa|number_of_bars], default=ratings
# It can only be called by companies, countries and regions. bars don't 
# have number_of_bars.
def cocoa_rating_numbers_of_bars(option_commands, query):
    late_query = ''
    # - [ratings|cocoa|number_of_bars], default=ratings
    # cocoa
    if 'cocoa' in option_commands:
        query += 'avg(CocoaPercent)'
        late_query = 'ORDER BY avg(CocoaPercent) '

    # number_of_bars
    elif 'number_of_bars' in option_commands:
        query += 'count(Company)'
        late_query = 'ORDER BY count(Company) '

    # ratings | default=ratings
    else:
        query += 'avg(Rating)'
        late_query = 'ORDER BY avg(Rating) '

    return late_query, query

# All the high level command accept: 
# - [top|bottom], default=top
# - <integer>, default=10
# This is a template for all the high level command to deal with these three
# parameters(top, bottom and integer)
def top_bottom_integer(option_commands, query, needToAddSecondOrder=False, Order=", Company ASC"):
    # - [top|bottom], default=top
    # bottom
    if 'bottom' in option_commands:
        query += 'ASC'

    # top | default=top
    else:
        query += 'DESC'

    # Here is for a second order like:
    # "companies region=Europe number_of_bars 12"
    # The output is:
    # |     Bonnat      |     France      |       27        |
    # |     Pralus      |     France      |       25        |
    # |    A. Morin     |     France      |       23        |
    # |     Domori      |      Italy      |       22        |
    # |    Valrhona     |     France      |       21        |
    # | Hotel Chocol... | United Kingd... |       19        |
    # |    Coppeneur    |     Germany     |       18        |
    # |     Zotter      |     Austria     |       17        |
    # | Artisan du C... | United Kingd... |       16        |
    # |  Szanto Tibor   |     Hungary     |       15        |
    # | Pierre Marco... |     Belgium     |       14        |
    # |     Duffy's     | United Kingd... |       13        | <----This line will be 
    # different if I set a second order like "Company ASC". It will change to
    # |     Amedei      |      Italy      |       13        |
    # Both of them have the same number_of_bars of 13. 
    # I only find this situation in this example(when using 'companies'), I decided 
    # to make my program's output exactly the same as examples provided in the pdf
    # However, the other high level commands' outputs are just the same as what pdf
    # provided. Then, I left them without setting specific second order. 
    if needToAddSecondOrder:
        query += Order

    # - <integer>, default=10
    useDefault = True
    for option in option_commands:

        # <integer>
        if option.isdigit():
            query += '\nLIMIT ' + option + '\n'
            useDefault = False

    # default=10
    if useDefault:
        query += '\nLIMIT 10\n'

    # You can uncomment this line to see what query the database is receiving
    # print(query)
    cur.execute(query)
    result = []
    for row in cur:
        result.append(row)
    return result

# High level command : bars
def bars(option_commands):
    query = '''SELECT a.SpecificBeanBarName, a.Company, b.EnglishName, a.Rating, a.CocoaPercent, c.EnglishName
FROM Bars a
JOIN Countries b ON b.Id = a.CompanyLocationId
JOIN Countries c ON c.Id = a.BroadBeanOriginId
'''

    # validating the option commands
    if not checkvalidatoin(option_commands, 0):
        return []

    # - [sell|source], default=sell
    # source
    local_query = ''
    if 'source' in option_commands:
        local_query += 'WHERE c.'
    # sell | defalut = sell
    else:
        local_query += 'WHERE b.'

    # - [none|country=<alpha2>|region=<name>], default=none
    for option in option_commands:
        # country=<alpha2>
        if 'country=' in option:
            country = option[8:]
            # check whether <alpha2> is valid
            if len(country) != 2:
                print('Please check your input, "' + country + '" is not a Alpha2 format')
                return []
            local_query += "Alpha2 = '" + country.upper() + "'\n"
        # region=<name>
        elif 'region=' in option:
            region = option[7:]
            # check whether <name> is valid
            if len(region) == 0:
                print('Please check your input, "' + region + '" should not be blank')
                return []
            local_query += "Region = '" + region + "'\n"
    if len(local_query) > 8:
        query += local_query

    # - [ratings|cocoa], default=ratings
    # cocoa
    if 'cocoa' in option_commands:
        query += 'ORDER BY a.CocoaPercent '
    # ratings | default=ratings
    else:
        query += 'ORDER BY a.Rating '

    # - [top|bottom], default=top
    # - <integer>, default=10
    return top_bottom_integer(option_commands, query)

# High level command : companies
def companyies(option_commands):
    query = 'SELECT Company, EnglishName, '

    # validating the option commands
    if not checkvalidatoin(option_commands, 1):
        return []

    # - [ratings|cocoa|number_of_bars], default=ratings
    late_query, query = cocoa_rating_numbers_of_bars(option_commands, query)

    query += '''
FROM (SELECT Company, EnglishName, CocoaPercent, Rating
FROM Bars
JOIN Countries ON Bars.CompanyLocationId = Countries.Id
'''
    # - [none|country=<alpha2>|region=<name>], default=none
    for option in option_commands:

        # country=<alpha2>
        if 'country=' in option:
            country = option[8:]

            # check whether <alpha2> is valid
            if len(country) != 2:
                print('Please check your input, "' + country + '" is not a Alpha2 format')
                return []
            query += "WHERE Alpha2 = '" + country.upper() + "'\n"

        # region=<name>
        elif 'region=' in option:
            region = option[7:]

            # check whether <name> is valid
            if len(region) == 0:
                print('Please check your input, "' + region + '" should not be blank')
                return []
            query += "WHERE Region = '" + region + "'\n"

    query += ''')GROUP BY Company
HAVING COUNT(Company) > 4
''' + late_query

    # - [top|bottom], default=top
    # - <integer>, default=10
    return top_bottom_integer(option_commands, query, needToAddSecondOrder=True)

def countries(option_commands):
    query = 'SELECT EnglishName, Region, '

    # validating the option commands
    if not checkvalidatoin(option_commands, 2):
        return []

    # - [ratings|cocoa|number_of_bars], default=ratings
    late_query, query = cocoa_rating_numbers_of_bars(option_commands, query)

    query += '''
FROM (SELECT EnglishName, Region, CocoaPercent, Rating, Company
FROM Countries
JOIN Bars ON Countries.Id = Bars.'''

    # - [sell|source], default=sell
    # source
    if 'source' in option_commands:
        query += 'BroadBeanOriginId\n'
    # sell | defalut = sell
    else:
        query += 'CompanyLocationId\n'

    # - [none|region=<name>], default=none
    for option in option_commands:
        # region=<name>
        if 'region=' in option:
            region = option[7:]
            # check whether <name> is valid
            if len(region) == 0:
                print('Please check your input, "' + region + '" should not be blank')
                return []
            query += "WHERE Region = '" + region + "'\n"

    query += ''')GROUP BY EnglishName
HAVING COUNT(Company) > 4
''' + late_query

    # - [top|bottom], default=top
    # - <integer>, default=10
    return top_bottom_integer(option_commands, query)

def regions(option_commands):
    query = 'SELECT Region, '

    # validating the option commands
    if not checkvalidatoin(option_commands, 3):
        return []

    # - [ratings|cocoa|number_of_bars], default=ratings
    late_query, query = cocoa_rating_numbers_of_bars(option_commands, query)

    query += '''
FROM (SELECT EnglishName, Region, CocoaPercent, Rating, Company
FROM Countries
JOIN Bars ON Countries.Id = Bars.'''

    # - [sell|source], default=sell
    # source
    if 'source' in option_commands:
        query += 'BroadBeanOriginId\n'
    # sell | defalut = sell
    else:
        query += 'CompanyLocationId\n'

    query += ''')GROUP BY Region
HAVING COUNT(Company) > 4
''' + late_query

    # - [top|bottom], default=top
    # - <integer>, default=10
    return top_bottom_integer(option_commands, query)

# Load the help file
def load_help_text():
    with open('Proj3Help.txt') as f:
        return f.read()

# Part 2 & 3: Implement interactive prompt and plotting. We've started for you!
def interactive_prompt():
    # Load for the help file to print help information
    help_text = load_help_text()
    
    # A String to store what the user input
    response = ''

    # Here is two variable to hold the previous command and the results to deal 
    # with the situation like :
    # "countries source region=Americas bottom 3"
    # "barplot" 
    pre_command = ''
    pre_data = []

    while True:
        response = input('Enter a command: ')
        # Here is for help information
        if response == 'help':
            print(help_text)
            continue
        
        # Here is for exiting 
        if response == 'exit':
            break

        # Here is for no input
        if len(response) == 0:
            print('')
            continue

        # Here is for barplot
        # Here is for the situation like:
        # "countries source region=Americas bottom 3"
        # "barplot" 
        # What's more, for the situation that nothing to plot
        if response == 'barplot' and len(pre_data) > 0:
            barplot(pre_command, pre_data)
            print('')
            continue
        if response == 'barplot' and len(pre_data) == 0:
            print('Nothing to plot!')
            print('')
            continue

        # store previous command and results
        tmp = process_command(response)
        if len(tmp) > 0:
            pre_data = tmp
            pre_command = response

        
    print("bye")

# barplot function
def barplot(command, data):
    xvals = []
    yvals = []

    # bars:
    # 0. Specific Bean Bar Name
    # 1. Company Name
    # 2. Company Location
    # 3. Rating
    # 4. Cocoa Percent
    # 5. Broad Bean Origin)
    # x-axis: Specific Bean Bar Name
    # y-axis: ratings or cocoa percentage (whichever was specified by the command)
    
    # companies:
    # 0. Company Name
    # 1. Company Location
    # 2. <agg: avg rating, avg cocoa, or number_of_bars>
    # x-axis: Company Name
    # y-axis: ratings/cocoa percentage/number_of_bars (whichever was specified)

    # countries:
    # 0. Country
    # 1. Region
    # 2. <agg: avg rating, avg cocoa, or number_of_bars>
    # x-axis: Country Name
    # y-axis: ratings/cocoa percentage/number_of_bars (whichever was specified)

    # regions:
    # 0. Region
    # 1. <agg: avg rating, avg cocoa, or number_of_bars>
    # x-axis: Region Name
    # y-axis: ratings/cocoa percentage/number_of_bars (whichever was specified)

    # default x-axis for all command is there first coloumn of the results, index = 0
    # default y-axis for bars is ratings and the index is 3
    xindex = 0
    yindex = 3

    # when ordered by coca percentage, yindex = 4
    if 'bars' in command and 'cocoa' in command:
        yindex = 4

    # when plotting for companies or countries, yindex = 2 
    elif 'companies' in command or 'countries' in command:
        yindex = 2
    # when plotting for regions, yindex = 1
    elif 'regions' in command:
        yindex = 1
    
    for index, ele in enumerate(data, start = 1):
        xvals.append(str(index) + '. ' + ele[xindex])
        yvals.append(ele[yindex])

    bar_data = go.Bar(x=xvals, y=yvals)
    fig = go.Figure(data=bar_data)
    fig.show()

# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    interactive_prompt()
