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
parameters_valid_part1 = [
    ['none', 'sell', 'source', 'ratings', 'cocoa', 'top', 'bottom'],
    ['none', 'ratings', 'cocoa', 'number_of_bars', 'top', 'bottom'],
    ['none', 'sell', 'source', 'ratings', 'cocoa', 'number_of_bars', 'top', 'bottom'],
    ['sell', 'source', 'ratings', 'cocoa', 'number_of_bars', 'top', 'bottom']
]
parameters_valid_part2 = [
    ['country=', 'region='],
    ['country=', 'region='],
    ['region='],
    [],
]

def process_command(command):
    
    query = command.split(' ')
    if len(query) != 0:
        high_level = decideHighLevelCommands(query[0])
        if not high_level:
            print("Command not recognized: " + command + '\n')
            return []
        if high_level == 1:
            output = bars(query[1:])
            tmp = list(output)
            if (len(output) != 0):
                for list_data in output:
                    tmp = list(list_data)
                    for i in [0, 1, 2, 5]:
                        if len(tmp[i]) > 12:
                            tmp[i] = tmp[i][:12] + '...'
                    print('| {:^15} | {:^15} | {:^15} | {:^15.1f} | {:^15.0%} | {:^15} |'.format(tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5]))
            print('')
            if 'barplot' in command:
                xvals = []
                yvals = []
                xindex = 0
                yindex = 3
                if 'cocoa' in command:
                    yindex = 4
                for ele in output:
                    xvals.append(ele[xindex])
                    yvals.append(ele[yindex])
                bar_data = go.Bar(x=xvals, y=yvals)
                fig = go.Figure(data=bar_data)
                fig.show()
            return output
        elif high_level == 2:
            output = companyies(query[1:])
            tmp = list(output)
            if (len(output) != 0):
                for list_data in output:
                    tmp = list(list_data)
                    for i in [0, 1]:
                        if len(tmp[i]) > 12:
                            tmp[i] = tmp[i][:12] + '...'
                    if isinstance(tmp[2], float):
                        tmp[2] = round(tmp[2], 1)
                    print('| {:^15} | {:^15} | {:^15} |'.format(tmp[0],tmp[1],tmp[2]))
            print('')
            if 'barplot' in command:
                xvals = []
                yvals = []
                xindex = 0
                yindex = 2
                for ele in output:
                    xvals.append(ele[xindex])
                    yvals.append(ele[yindex])
                bar_data = go.Bar(x=xvals, y=yvals)
                fig = go.Figure(data=bar_data)
                fig.show()
            return output
        elif high_level == 3:
            output = countries(query[1:])
            tmp = list(output)
            if (len(output) != 0):
                for list_data in output:
                    tmp = list(list_data)
                    for i in [0, 1]:
                        if len(tmp[i]) > 12:
                            tmp[i] = tmp[i][:12] + '...'
                    if isinstance(tmp[2], float):
                        tmp[2] = round(tmp[2], 1)
                    print('| {:^15} | {:^15} | {:^15} |'.format(tmp[0],tmp[1],tmp[2]))
            print('')
            if 'barplot' in command:
                xvals = []
                yvals = []
                xindex = 0
                yindex = 2
                for ele in output:
                    xvals.append(ele[xindex])
                    yvals.append(ele[yindex])
                bar_data = go.Bar(x=xvals, y=yvals)
                fig = go.Figure(data=bar_data)
                fig.show()
            return output
        else:
            output = regions(query[1:])
            tmp = list(output)
            if (len(output) != 0):
                for list_data in output:
                    tmp = list(list_data)
                    if len(tmp[0]) > 12:
                        tmp[0] = tmp[0][:12] + '...'
                    if isinstance(tmp[1], float):
                        tmp[1] = round(tmp[1], 1)
                    print('| {:^15} | {:^15} |'.format(tmp[0],tmp[1]))
            print('')
            if 'barplot' in command:
                xvals = []
                yvals = []
                xindex = 0
                yindex = 1
                for ele in output:
                    xvals.append(ele[xindex])
                    yvals.append(ele[yindex])
                bar_data = go.Bar(x=xvals, y=yvals)
                fig = go.Figure(data=bar_data)
                fig.show()
            return output
    return []

def decideHighLevelCommands(opeartion):
    if (opeartion == 'bars'):
        return 1
    elif (opeartion == 'companies'):
        return 2
    elif (opeartion == 'countries'):
        return 3
    elif (opeartion == 'regions'):
        return 4
    else:
        return 0

def checkvalidatoin(option_commands, type):
    # validating the option commands
    for option in option_commands:
        if option in parameters_valid_part1[type] or option.isdigit() or option == 'barplot':
            continue
        bFind = False
        for ele in parameters_valid_part2[type]:
            if ele in option:
                bFind = True
                break
        if (bFind):
            continue
        print('Please check your input, "' + option +'" is invalid.')
        return False
    return True

def cocoa_rating_numbers_of_bars(option_commands, query):
    late_query = ''
    # - [ratings|cocoa], default=ratings
    # cocoa
    if 'cocoa' in option_commands:
        query += 'avg(CocoaPercent)'
        late_query = 'ORDER BY avg(CocoaPercent) '
    # ratings | default=ratings
    elif 'number_of_bars' in option_commands:
        query += 'count(Company)'
        late_query = 'ORDER BY count(Company) '
    else:
        query += 'avg(Rating)'
        late_query = 'ORDER BY avg(Rating) '

    return late_query, query

def top_bottom_integer(option_commands, query):
    # - [top|bottom], default=top
    # bottom
    if 'bottom' in option_commands:
        query += 'ASC\n'
    # ratings | default=ratings
    else:
        query += 'DESC\n'

    useDefault = True
    # - <integer>, default=10
    for option in option_commands:
        # <integer>
        if option.isdigit():
            query += 'LIMIT ' + option + '\n'
            useDefault = False
    # default=10
    if useDefault:
        query += 'LIMIT 10\n'
    #print(query)
    cur.execute(query)
    result = []
    for row in cur:
        result.append(row)
    return result

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

    # - [none|country=<alpha2>| region=<name>], default=none
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

    return top_bottom_integer(option_commands, query)

def companyies(option_commands):
    query = 'SELECT Company, EnglishName, '
    # validating the option commands
    if not checkvalidatoin(option_commands, 1):
        return []
    
    late_query, query = cocoa_rating_numbers_of_bars(option_commands, query)

    query += '''
FROM (SELECT Company, EnglishName, CocoaPercent, Rating
FROM Bars
JOIN Countries ON Bars.CompanyLocationId = Countries.Id
'''
    # - [none|country=<alpha2>| region=<name>], default=none
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

    return top_bottom_integer(option_commands, query)

def countries(option_commands):
    query = 'SELECT EnglishName, Region, '

    # validating the option commands
    if not checkvalidatoin(option_commands, 2):
        return []

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

    # - [none|country=<alpha2>| region=<name>], default=none
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

    return top_bottom_integer(option_commands, query)

def regions(option_commands):
    query = 'SELECT Region, '
    print(option_commands)

    # validating the option commands
    if not checkvalidatoin(option_commands, 3):
        return []
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

    return top_bottom_integer(option_commands, query)

def load_help_text():
    with open('Proj3Help.txt') as f:
        return f.read()

# Part 2 & 3: Implement interactive prompt and plotting. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    pre_command = ''
    pre_data = []
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print(help_text)
            continue
        if len(response) == 0:
            print('')
            continue
        if response == 'barplot' and len(pre_data) > 0:
            xvals = []
            yvals = []
            xindex = 0
            yindex = 3
            if 'bars' in pre_command and 'cocoa' in command:
                yindex = 4
            elif 'companies' in pre_command or 'countries' in pre_command:
                yindex = 2
            elif 'regions' in pre_command:
                yindex = 1
            for ele in pre_data:
                xvals.append(ele[xindex])
                yvals.append(ele[yindex])
            bar_data = go.Bar(x=xvals, y=yvals)
            fig = go.Figure(data=bar_data)
            fig.show()
            print('')
            continue
        pre_data = process_command(response)
        pre_command = response

        
    print("bye")

# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    interactive_prompt()
