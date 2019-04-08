#Importing basic libs
import numpy as np
import pandas as pd

#############################################################

#Importing data
data = pd.read_csv('athlete_events.csv')
noc_country = pd.read_csv('noc_regions.csv')

#Cleaning data
data["Medal"].fillna('DNW',inplace=True)
noc_country.drop('notes',axis=1,inplace=True)
noc_country.rename(columns={'region':'Country'},inplace=True)

#Merging data
olym_merge = data.merge(noc_country,
                        left_on = 'NOC',
                        right_on = 'NOC',
                        how = 'left')
olym_merge.loc[olym_merge['Country'].isnull(),['NOC', 'Team']].drop_duplicates()

#Replacing missing Teams by the values above.
olym_merge['Country'] = np.where(olym_merge['NOC']=='SGP', 'Singapore', olym_merge['Country'])
olym_merge['Country'] = np.where(olym_merge['NOC']=='ROT', 'Refugee Olympic Athletes', olym_merge['Country'])
olym_merge['Country'] = np.where(olym_merge['NOC']=='UNK', 'Unknown', olym_merge['Country'])
olym_merge['Country'] = np.where(olym_merge['NOC']=='TUV', 'Tuvalu', olym_merge['Country'])

#Putting these values from Country into Team
olym_merge.drop('Team', axis = 1, inplace = True)
olym_merge.rename(columns = {'Country': 'Team'}, inplace = True)

#only GDP from 1961 onwards are taken
w_gdp = pd.read_csv('world_gdp.csv', skiprows = 3)
w_gdp.drop(['Indicator Name', 'Indicator Code'], axis = 1, inplace = True)
w_gdp = pd.melt(w_gdp, id_vars = ['Country Name', 'Country Code'], var_name = 'Year', value_name = 'GDP')
w_gdp['Year'] = pd.to_numeric(w_gdp['Year'])

#Merging to get country code
olympics_merge_ccode = olym_merge.merge(w_gdp[['Country Name', 'Country Code']].drop_duplicates(),
                                            left_on = 'Team',
                                            right_on = 'Country Name',
                                            how = 'left')

olympics_merge_ccode.drop('Country Name', axis = 1, inplace = True)

#Merging to get gdp too
olympics_merge_complete = olympics_merge_ccode.merge(w_gdp,
                                                left_on = ['Country Code', 'Year'],
                                                right_on = ['Country Code', 'Year'],
                                                how = 'left')

olympics_merge_complete.drop('Country Name', axis = 1, inplace = True)

#Taking 1961 summer olympics onwards
olympics_complete_subset = olympics_merge_complete.loc[(olym_merge['Year'] > 1960)&(olympics_merge_complete['Season'] == "Summer"), :]
olympics_complete_subset = olympics_complete_subset.reset_index()

#Height, Weight, Age Cleaning
olympicDataClean = pd.DataFrame(olympics_complete_subset[ olympics_complete_subset['Height'].notnull() ])
olympicDataClean = pd.DataFrame(olympicDataClean[ olympicDataClean['Weight'].notnull() ])
olympicDataClean = pd.DataFrame(olympicDataClean[ olympicDataClean['Age'].notnull() ])
olympicDataClean['Medal_Won'] = np.where(olympicDataClean.loc[:,'Medal'] == 'DNW', 0, 1)

#Check whether number of medals won in a year for an event by a team exceeds 1. This indicates a team event.
identify_team_events = pd.pivot_table(olympicDataClean,
                                      index = ['Team', 'Year', 'Event'],
                                      columns = 'Medal',
                                      values = 'Medal_Won',
                                      aggfunc = 'sum',
                                     fill_value = 0).drop('DNW', axis = 1).reset_index()

identify_team_events = identify_team_events.loc[identify_team_events['Gold'] > 1, :]

team_sports = identify_team_events['Event'].unique()

# if an event name matches with one in team sports, then it is a team event. Others are singles events.
team_event_mask = olympicDataClean['Event'].map(lambda x: x in team_sports)
single_event_mask = [not i for i in team_event_mask]

# rows where medal_won is 1
medal_mask = olympicDataClean['Medal_Won'] == 1

# Put 1 under team event if medal is won and event in team event list
olympicDataClean['Team_Event'] = np.where(team_event_mask & medal_mask, 1, 0)

# Put 1 under singles event if medal is won and event not in team event list
olympicDataClean['Single_Event'] = np.where(single_event_mask & medal_mask, 1, 0)

# Add an identifier for team/single event
olympicDataClean['Event_Category'] = olympicDataClean['Single_Event'] + \
olympicDataClean['Team_Event']

medal_tally_agnostic = olympicDataClean.\
groupby(['Year', 'Team', 'Event', 'Medal'])[['Medal_Won', 'Event_Category']].\
agg('sum').reset_index()

medal_tally_agnostic['Medal_Won_Corrected'] = medal_tally_agnostic['Medal_Won']/medal_tally_agnostic['Event_Category']

# Medal Tally.
medal_tally = medal_tally_agnostic.groupby(['Year','Team'])['Medal_Won_Corrected'].agg('sum').reset_index()

medal_tally_pivot = pd.pivot_table(medal_tally,
                     index = 'Team',
                     columns = 'Year',
                     values = 'Medal_Won_Corrected',
                     aggfunc = 'sum',
                     margins = True).sort_values('All', ascending = False)

medal_tally_pivot_All = pd.DataFrame(medal_tally_pivot['All'])
medal_tally_pivot_All.reset_index(inplace = True)

#Getting country code and name, gonna merge it with medal count
country_and_noc = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
country_and_noc = country_and_noc.replace('United States', 'USA')

#merging medal count and country code
country_noc_medal = country_and_noc.merge(medal_tally_pivot_All, left_on='COUNTRY',right_on='Team')
country_noc_medal = country_noc_medal.replace('United States', 'USA')

#Medal tally and GDP correlation
# List of top countries
top_countries = ['USA', 'Russia', 'Germany', 'China']

year_team_medals = pd.pivot_table(medal_tally,
                                  index = 'Year',
                                  columns = 'Team',
                                  values = 'Medal_Won_Corrected',
                                  aggfunc = 'sum')[top_countries]



# List of top countries
top_countries = ['USA', 'Russia', 'Germany', 'China']

# row mask where countries match
row_mask_2 = medal_tally_agnostic['Team'].map(lambda x: x in top_countries)

# Pivot table to calculate sum of gold, silver and bronze medals for each country
medal_tally_specific = pd.pivot_table(medal_tally_agnostic[row_mask_2],
                                     index = ['Team'],
                                     columns = 'Medal',
                                     values = 'Medal_Won_Corrected',
                                     aggfunc = 'sum',
                                     fill_value = 0).drop('DNW', axis = 1)

# Re-order the columns so that they appear in order on the chart.
medal_tally_specific = medal_tally_specific.loc[:, ['Gold', 'Silver', 'Bronze']]

# To get the sports, teams are best at, we now aggregate the medal_tally_agnostic dataframe as we did earlier.
best_team_sports = pd.pivot_table(medal_tally_agnostic[row_mask_2],
                                  index = ['Team', 'Event'],
                                  columns = 'Medal',
                                  values = 'Medal_Won_Corrected',
                                  aggfunc = 'sum',
                                  fill_value = 0).sort_values(['Team', 'Gold'], ascending = [True, False]).reset_index()

best_team_sports.drop(['Bronze', 'Silver', 'DNW'], axis = 1, inplace = True)
best_team_sports.columns = ['Team', 'Event', 'Gold_Medal_Count']

# To get the sports, teams are best at, we now aggregate the medal_tally_agnostic dataframe as we did earlier.
best_team_sports = pd.pivot_table(medal_tally_agnostic[row_mask_2],
                                  index = ['Team', 'Event'],
                                  columns = 'Medal',
                                  values = 'Medal_Won_Corrected',
                                  aggfunc = 'sum',
                                  fill_value = 0).sort_values(['Team', 'Gold'], ascending = [True, False]).reset_index()

best_team_sports.drop(['Bronze', 'Silver', 'DNW'], axis = 1, inplace = True)
best_team_sports.columns = ['Team', 'Event', 'Gold_Medal_Count']

# merge best team sports with olympics data to get sport for each event.
team_commonalities = best_team_sports.merge(olympicDataClean.loc[:,['Sport', 'Event']].drop_duplicates(),
                                           left_on = 'Event',
                                           right_on = 'Event')

team_commonalities = team_commonalities.sort_values(['Team', 'Gold_Medal_Count'], ascending = [True, False])
team_commonalities = team_commonalities.groupby('Team').head(5).reset_index()

# make a pivot table of the commonalities.
pd.pivot_table(team_commonalities,
              index = 'Sport',
              columns = 'Team',
              values = 'Event',
              aggfunc = 'count',
              fill_value = 0,
              margins = True).sort_values('All', ascending = False)[1:]

olympicDataClean[['Year', 'City']].drop_duplicates().sort_values('Year')

# Correct city names in the dataset
olympicDataClean['City'].replace(['Athina', 'Moskva'], ['Athens', 'Moscow'], inplace = True)

# city to country mapping dictionary
city_to_country = {'Tokyo': 'Japan',
                  'Mexico City': 'Mexico',
                  'Munich': 'Germany',
                  'Montreal': 'Canada',
                  'Moscow': 'Russia',
                  'Los Angeles': 'USA',
                  'Seoul': 'South Korea',
                  'Barcelona': 'Spain',
                  'Atlanta': 'USA',
                  'Sydney': 'Australia',
                  'Athens': 'Greece',
                  'Beijing': 'China',
                  'London': 'UK',
                  'Rio de Janeiro': 'Brazil'}

# Map cities to countries
olympicDataClean['Country_Host'] = olympicDataClean['City'].map(city_to_country)

#print the 
olympicDataClean.loc[:, ['Year', 'Country_Host']].drop_duplicates().sort_values('Year')

# Extract year, host nation and team name from the data
year_host_team = olympicDataClean[['Year', 'Country_Host', 'Team']].drop_duplicates()

# check rows where host country is the same as team
row_mask_4 = (year_host_team['Country_Host'] == year_host_team['Team'])

# add years in the year_host_team to capture one previous and one later year
year_host_team['Prev_Year'] = year_host_team['Year'] - 4
year_host_team['Next_Year'] = year_host_team['Year'] + 4

# Subset only where host nation and team were the same
year_host_team = year_host_team[row_mask_4]

# Calculate the medals won in each year where a team played at home. merge year_host_team with medal_tally on year and team
year_host_team_medal = year_host_team.merge(medal_tally,
                                           left_on = ['Year', 'Team'],
                                           right_on = ['Year', 'Team'],
                                           how = 'left')

year_host_team_medal.rename(columns = {'Medal_Won_Corrected' : 'Medal_Won_Host_Year'}, inplace = True)

# Calculate medals won by team in previous year
year_host_team_medal = year_host_team_medal.merge(medal_tally,
                                                 left_on = ['Prev_Year', 'Team'],
                                                 right_on = ['Year', 'Team'],
                                                 how = 'left')

year_host_team_medal.drop('Year_y', axis = 1, inplace = True)
year_host_team_medal.rename(columns = {'Medal_Won_Corrected': 'Medal_Won_Prev_Year',
                                      'Year_x':'Year'}, inplace = True)

# Calculate the medals won by the team the year after they hosted.
year_host_team_medal = year_host_team_medal.merge(medal_tally,
                                                 left_on = ['Next_Year', 'Team'],
                                                 right_on = ['Year', 'Team'],
                                                 how = 'left')

year_host_team_medal.drop('Year_y', axis = 1, inplace = True)
year_host_team_medal.rename(columns = {'Year_x': 'Year',
                                      'Medal_Won_Corrected' : 'Medal_Won_Next_Year'}, inplace = True)

# General formatting changes
year_host_team_medal.drop(['Prev_Year', 'Next_Year'], axis = 1, inplace = True)
year_host_team_medal.sort_values('Year', ascending = True, inplace = True)
year_host_team_medal.reset_index(inplace = True, drop = True)

# column re-ordering
year_host_team_medal = year_host_team_medal.loc[:, ['Year', 'Country_Host', 'Team', 'Medal_Won_Prev_Year', 'Medal_Won_Host_Year', 'Medal_Won_Next_Year']]

year_team_gdp = olympics_complete_subset.loc[:, ['Year', 'Team', 'GDP']].drop_duplicates()

medal_tally_gdp = medal_tally.merge(year_team_gdp,
                                   left_on = ['Year', 'Team'],
                                   right_on = ['Year', 'Team'],
                                   how = 'left')

#adding medal in numeric value
def score_to_numeric(x):
    if x=='Gold':
        return 3
    if x=='Silver':
        return 2
    if x=='Bronze':
        return 1
    
    
olympicDataClean['Medal_num'] = olympicDataClean['Medal'].apply(score_to_numeric)
olympicDataClean["Medal_num"].fillna(0,inplace=True)

#export
export_country_noc_medal = country_noc_medal
export_data = olympicDataClean
export_medal_tally_gdp = medal_tally_gdp
