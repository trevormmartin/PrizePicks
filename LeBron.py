import matplotlib.pyplot as plt
import seaborn as sns
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.static import players
import numpy as np
import time
import pandas as pd
from datetime import date, timedelta
from tqdm import tqdm

# get LeBron game logs
game_logs = playergamelogs.PlayerGameLogs(
    season_nullable="2022-23", player_id_nullable=players.find_players_by_full_name("LeBron James")[0]['id'])

# pandas data frames
df = game_logs.get_data_frames()[0][["PLAYER_NAME", "GAME_DATE", "MATCHUP", "WL", "MIN", "FGM",
                                    "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA",
                                     "FT_PCT", "OREB", "DREB", "REB", "AST", "TOV", "STL",
                                     "BLK", "BLKA", "PF", "PFD", "PTS"]]

# add PP stats
df["PTS+REBS+ASTS"] = df["PTS"] + df["REB"] + df["AST"]
df["PTS+REBS"] = df["PTS"] + df["REB"]
df["PTS+ASTS"] = df["PTS"] + df["AST"]
df["REBS+ASTS"] = df["REB"] + df["AST"]
df["BLK+STL"] = df["BLK"] + df["STL"]
df["FANTASY"] = df["PTS"] + 1.2*df["REB"] + 1.5 * \
    df["AST"] + 3*df["BLK"] + 3*df["STL"] - df["TOV"]

df['HOME'] = np.where(df['MATCHUP'].str[4] == '@', 'Away', 'Home')
df['Opponent'] = df['MATCHUP'].str[-3:]

# fix date formatting
df['DATE'] = pd.to_datetime(df['GAME_DATE']).dt.date

df['REST_DAYS'] = df.sort_values('DATE').groupby(
    'PLAYER_NAME')['DATE'].diff() / np.timedelta64(1, 'D')

print(df)

sns.scatterplot(x="MIN",       # x variable name
                y="REB",       # y variable name
                hue="HOME",  # group variable name
                data=df,     # dataframe to plot
                )

plt.show()
