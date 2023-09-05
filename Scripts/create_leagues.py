import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import itertools
import time

def add_blank_rows(df, no_rows):
    df_new = pd.DataFrame(columns=df.columns)
    for idx in range(len(df)):
        df_new = df_new.append(df.iloc[idx])
        for _ in range(no_rows):
            df_new=df_new.append(pd.Series(), ignore_index=True)
    return df_new

def distribute_teams(team_names, num_leagues):
    if num_leagues <= 0:
        raise ValueError("Number of leagues must be greater than zero")
    
    team_names.sort()  # Sort team names alphabetically
    league_dict = {}

    for i, team_name in enumerate(team_names):
        league_name = chr(ord('A') + (i % num_leagues))  # Distribute teams to leagues in order (A, B, C, ...)
        league_dict[team_name] = league_name

    return league_dict

def group_teams_by_league(teams_dict):
    # Create an empty dictionary to store teams grouped by league
    teams_by_league = {}
    
    # Iterate through the teams in the input dictionary
    for team, league in teams_dict.items():
        # Check if the league code is already in the teams_by_league dictionary
        if league in teams_by_league:
            # If it's already in the dictionary, append the team to the corresponding list
            teams_by_league[league].append(team)
        else:
            # If it's not in the dictionary, create a new list with the team
            teams_by_league[league] = [team]
    
    # Convert the dictionary values (lists of teams) to a list of lists
    league_lists = list(teams_by_league.values())
    
    return league_lists

def generate_fixture_schedule(teams):
    matchups = itertools.combinations(teams, 2)
    #random.shuffle(matchups)
    
    schedule = pd.DataFrame(columns=['H', '', 'v', ' ', 'B', 'Dato', 'Kl', 'Bane', 'Dommer'])
    
    for i, (home_team, away_team) in enumerate(matchups):
        home_goals = None
        v = None
        away_goals = None
        date = None
        time = None
        location = None
        referee = None
        
        schedule.loc[i] = [home_team, home_goals, v, away_goals, away_team, date, time, location, referee]
    
    return schedule

def sort_schedule(schedule, team_list, n_teams):

    odd = False
    if n_teams%2 != 0:
        odd = True
    schedule0 = schedule
    new_schedule = pd.DataFrame(columns=['H', '', 'v', ' ', 'B', 'Dato', 'Kl', 'Bane', 'Dommer'])
    rounds = n_teams - 1
    if odd:
        rounds += 1
    schedule = schedule.sample(frac=1)
    if odd:
        passed = []

    for i in range(rounds):
        
        old_schedule = new_schedule
        time0 = time.time()
        while True:
            played = []
            dropping = []
            for j in range(schedule.shape[0]):
                if not schedule.iloc[j,0] in played and not schedule.iloc[j,4] in played:
                    row = pd.DataFrame(schedule.iloc[j,:]).T
                    if i % 2 != 0:
                        row.iloc[0,0], row.iloc[0,4] = row.iloc[0,4], row.iloc[0,0]
                    new_schedule = pd.concat([new_schedule, row])
                    played.append(schedule.iloc[j,0])
                    played.append(schedule.iloc[j,4])
                    dropping.append(schedule.index[j])
                if len(played) == n_teams:
                    break
            if odd:
                passing = list(set(team_list).difference(played))
            if time.time() - time0 > 4:
                print("Timed out, trying again")
                return sort_schedule(schedule0, team_list, n_teams)
            if odd and (len(played) != n_teams - 1 or passing in passed):
                new_schedule = old_schedule
                schedule = schedule.sample(frac=1)
            elif odd:
                passed.append(passing)
                break
            if len(played) != n_teams:
                new_schedule = old_schedule
                schedule = schedule.sample(frac=1)
            else:
                break
        schedule = schedule.drop(dropping)

    print(schedule)
    return new_schedule

team_list = [
    "Wolves of Ballstreet",
    "NTNUI Champs",
    "Salt IF",
    "Marin FK",
    "TIHLDE Pythons",
    "MiT Fotball",
    "Janus FK",
    "Erudio Herrer",
    "Smøreguttene FK",
    "Datakameratene FK",
    "Energi FK",
    "Tim&Shænko",
    "NTNUI Samba",
    "Pareto FK",
    "Realkameratene FK",
    "FK Steindølene 1",
    "Petroleum FK",
    "Omega løkka",
    "FK Steindølene 2",
    "Omega FK",
    "Hybrida FK",
    "Handelshøyskolen Sportsklubb (HSK)",
    "Chemie FK",
    "Knekken",
    "Hattfjelldal United",
    "Caf",
    "FK Hånd Til Munn"
]
n_leagues = 2

def main():
    leagues = distribute_teams(team_list, n_leagues)
    for team_list in group_teams_by_league(leagues):
        fixture_schedule = generate_fixture_schedule(team_list)
        schedule = sort_schedule(fixture_schedule, team_list, len(team_list))
        schedule.to_excel(f"Avd {leagues[team_list[0]]} - Kampoppsett.xlsx", index=False)
        print("JIPPI")

if __name__ == "__main__":
    main()