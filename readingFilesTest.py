import pandas as pd

df = pd.read_csv("team_batting.csv")
df_advanced_pitchers = pd.read_csv("player_advanced_pitching.csv")
df_standard_pitchers = pd.read_csv("player_standard_pitching.csv")
df_batting_against = pd.read_csv("player_batting_against.csv")

# This will ask the user for the pitcher to evaluate and the team that they are facing and store the k% for the opposing team to be used in estimations

# Sometimes there is a pitcher with an asterick and it is stored different - so have to catch and take care of that error
user_pitcher_in_question = input("Enter the name of the pitcher to evaluate: ").strip() # strip gets rid of leading and trailing whitespaces
user_opposing_team = input("Enter the team that is playing against that pitcher: ").strip()
row_name = "Chicago Cubs"
column_name = "SO%"


# opposing_team_k_percent = df.loc[df.iloc[:, 0] == user_opposing_team, column_name]
team_row = df[df['Tm'] == user_opposing_team]
opposing_team_k_percent = team_row['SO%'].iloc[0]
# opposing_team_k_percent = opposing_team_k_percent.replace('%', '').astype(float)

# Getting the k% for the specific player (the player that was entered by the user beforehand i.e - user_pitcher_in_question)
pitcher_row = df_advanced_pitchers[df_advanced_pitchers['Name'] == user_pitcher_in_question]
if pitcher_row.empty:
    new_name = user_pitcher_in_question + "*"
    pitcher_row = df_advanced_pitchers[df_advanced_pitchers['Name'] == new_name]


pitcher_k_percent = pitcher_row['SO%'].str.replace('%', '').astype(float)

# Need to calculate the expected innings and batters faced by the pitcher for this game
player_row = df_standard_pitchers[df_standard_pitchers['Name'] == user_pitcher_in_question]
if player_row.empty:
    new_name = user_pitcher_in_question + "*"
    player_row = df_standard_pitchers[df_standard_pitchers['Name'] == new_name]

pitcher_games_started = (player_row['GS'].iloc[0]) # This gives me the number of games that the pitcher has started
pitcher_total_games = player_row['G'].iloc[0]  # This gives the total number of games that they have appeared in (gets more accurate projections)
pitcher_innings_pitched = (player_row['IP'].iloc[0]) # This gives me the number of innings pitched by that pitcher
pitcher_k_per_nine = player_row['SO9'].iloc[0] # strikeouts per nine innnings pitched


avg_ip_per_game = float(pitcher_innings_pitched) / float(pitcher_total_games)
# print("Their average innings pitched per game is: ", avg_ip_per_game)
percent_of_game_pitched = avg_ip_per_game / 9
pitcher_projection = percent_of_game_pitched * float(pitcher_k_per_nine) # THIS IS 1/2 OF THE PROJECTION
# print(pitcher_expected_strikeouts)

# Getting the number of AB's for a pitcher as it is better than PA's for strikeout purposes
player_row = df_batting_against[df_batting_against['Name'] == user_pitcher_in_question]
if player_row.empty:
    new_name = user_pitcher_in_question + "*"
    player_row = df_batting_against[df_batting_against['Name'] == new_name]

pitcher_ab_total = (player_row['AB'].iloc[0])
pitcher_pa_total = (player_row['PA'].iloc[0])

# Getting the expected batters faced in game (total PA's / total games (games appeared))
expected_pa = float(pitcher_pa_total) / float(pitcher_total_games)

# Need to take out the percent sign
opposing_team_k_percent = opposing_team_k_percent.replace('%', '')
opp_percent = float(opposing_team_k_percent) / 100   # this is the k percent in decimal form

opposing_team_projection = opp_percent * expected_pa # THIS IS THE OTHER 1/2 TO THE PROJECTION

print(opposing_team_projection)

# I now need to get the projection given the difference in calculations
#
# print("first value: ", pitcher_projection)
# print("second value: ", opposing_team_projection)


middle_ground_projection = ((pitcher_projection + opposing_team_projection) / 2)

print("middle ground projection is: ", middle_ground_projection)