from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.views import View
# from .forms import decadeForm
# from .models import chooseDecade
from bs4 import BeautifulSoup
import requests
import pandas as pd

DECADE_OPTIONS = [
    '1950s',
    '1960s',
    '1970s',
    '1980s',
    '1990s',
    '2000s',
    '2010s',
    'Planned_or_scheduled'
]

#============== Rendering page with decade options for user to choose from
def space_exploration(request):
    decades = {'decades' : DECADE_OPTIONS}
    return render(request, 'explorationTimeline/space_exploration.html', decades)


#============== Using BeautifulSoup to get tables from Wikipage based on user selected decade
def result(request, decade):  #pass the user selected variable 'decade' into the function
    print("Decade selected: " + str(decade)) #prints to console for development purposes
    getPage = requests.get("https://en.wikipedia.org/wiki/Timeline_of_Solar_System_exploration") #get the page
    src = getPage.content #store the page's contents as a variable
    soup = BeautifulSoup(src, 'html.parser') #parse the content of the page
    missionsTable = soup.find(id= decade).findNext('table', {"class" : "wikitable"}) # get the requested table by looking at the table after the table headline   
    #print(missionsTable)

    create_table = [['Mission Name', 'Launch Date', 'Country', 'Wikipage']] #create list to put extracted data into
    rows = missionsTable.find_all('tr')[1:] #extract all rows except the first row because it is a header

    for row in rows: #loop through all the rows to extract desired data
        if decade in ('1950s', '1960s', '1970s'):
            mission_name = row.find_all('a')[1].get_text() #extract mission name
            wiki_link = 'https://en.m.wikipedia.org' + row.find_all('a')[1].get('href') # extract href
        elif decade in ('1980s', '1990s', '2000s', '2010s', 'Planned_or_scheduled'):
            mission_name = row.td.find('a', recursive= False).get_text() #extract mission name
            wiki_link = 'https://en.m.wikipedia.org' + row.td.find('a', recursive= False).get('href') # extract href
        launch_date = row.find_all('td')[1].get_text()[:-1]
        country = row.find('a').get('title')
        wikipage= '<a href="' + wiki_link + '">More Info</a>' # concatenate href to create link to mission wikipage
        display_row = [mission_name, launch_date, country, wikipage] # create a row
        create_table.append(display_row) # add the rows to the table

    df = pd.DataFrame(create_table[1:], columns = create_table[0]) #create table via Pandas module
    data = df.to_html(escape = False) #convert table to html
    #print(data)
    context = {
        'data' : data,
        'decade': decade,
    }
    return render(request, 'explorationTimeline/result.html', context)



