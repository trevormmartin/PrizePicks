from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.static import players
import numpy as np
import time
import pandas as pd
from datetime import date, timedelta
from tqdm import tqdm

# initialize lists to create dataframe later
player_names = []
player_stats = []
player_lines = []
season_overs = []
season_unders = []
L10_overs = []
L10_unders = []
L2W_overs = []
L2W_unders = []

# get distinct list of players in PrizePicks today
# fetch PP lines
timestr = time.strftime("%Y%m%d")
dp = pd.read_csv(r"./PrizePicks/Datasets/" + timestr + "_pp.csv")

dp = dp[dp["Name"].str.contains("+", regex=False) == False]

pp_players = dp["Name"].unique()

print(pp_players)
"""
game_logs = playergamelogs.PlayerGameLogs(
    season_nullable="2022-23",
    season_type_nullable="Playoffs",
    player_id_nullable=players.find_player_by_id("1628404"),
)

print(game_logs)
"""
for p in tqdm(pp_players, desc="Progress"):
    # Choose the Player to get stats for
    player_name = p
    print(p)
    if player_name == "OG Anunoby":
        game_logs = playergamelogs.PlayerGameLogs(
            season_nullable="2022-23",
            season_type_nullable="Playoffs",
            player_id_nullable=players.find_players_by_last_name("Anunoby")[0]["id"],
        )
    elif player_name == "Nicolas Claxton":
        game_logs = playergamelogs.PlayerGameLogs(
            season_nullable="2022-23",
            season_type_nullable="Playoffs",
            player_id_nullable=players.find_players_by_full_name("Nic Claxton")[0][
                "id"
            ],
        )
    elif player_name == "Joel Embiid":
        game_logs = playergamelogs.PlayerGameLogs(
            season_nullable="2022-23",
            season_type_nullable="Playoffs",
            player_id_nullable=players.find_player_by_id("203954"),
        )
    elif player_name == "Jayson Tatum":
        game_logs = playergamelogs.PlayerGameLogs(
            season_nullable="2022-23",
            season_type_nullable="Playoffs",
            player_id_nullable=players.find_player_by_id("1628369"),
        )
    elif player_name == "Jaylen Brown":
        game_logs = playergamelogs.PlayerGameLogs(
            season_nullable="2022-23",
            season_type_nullable="Playoffs",
            player_id_nullable=players.find_player_by_id("1627759"),
        )
    elif player_name == "Malcolm Brogdon":
        game_logs = playergamelogs.PlayerGameLogs(
            season_nullable="2022-23",
            season_type_nullable="Playoffs",
            player_id_nullable=players.find_player_by_id("1627763"),
        )
    elif player_name == "Andrew Wiggins":
        game_logs = playergamelogs.PlayerGameLogs(
            season_nullable="2022-23",
            season_type_nullable="Playoffs",
            player_id_nullable=players.find_player_by_id("203954"),
        )
    elif player_name == "Josh Hart":
        game_logs = playergamelogs.PlayerGameLogs(
            season_nullable="2022-23",
            season_type_nullable="Playoffs",
            player_id_nullable=players.find_player_by_id("1628404"),
        )
    elif player_name == "KJ Martin Jr.":
        game_logs = playergamelogs.PlayerGameLogs(
            season_nullable="2022-23",
            season_type_nullable="Playoffs",
            player_id_nullable=players.find_players_by_full_name("Kenyon Martin Jr.")[
                0
            ]["id"],
        )
    elif player_name == "D'Angelo Russell":
        game_logs = playergamelogs.PlayerGameLogs(
            season_nullable="2022-23",
            season_type_nullable="Playoffs",
            player_id_nullable=players.find_player_by_id("1626156"),
        )
    else:
        game_logs = playergamelogs.PlayerGameLogs(
            season_nullable="2022-23",
            season_type_nullable="Playoffs",
            player_id_nullable=players.find_players_by_full_name(player_name)[0]["id"],
        )

    # pandas data frames
    df = game_logs.get_data_frames()[0][
        [
            "PLAYER_NAME",
            "GAME_DATE",
            "MATCHUP",
            "WL",
            "MIN",
            "FGM",
            "FGA",
            "FG_PCT",
            "FG3M",
            "FG3A",
            "FG3_PCT",
            "FTM",
            "FTA",
            "FT_PCT",
            "OREB",
            "DREB",
            "REB",
            "AST",
            "TOV",
            "STL",
            "BLK",
            "BLKA",
            "PF",
            "PFD",
            "PTS",
        ]
    ]

    # add PP stats
    df["PTS+REBS+ASTS"] = df["PTS"] + df["REB"] + df["AST"]
    df["PTS+REBS"] = df["PTS"] + df["REB"]
    df["PTS+ASTS"] = df["PTS"] + df["AST"]
    df["REBS+ASTS"] = df["REB"] + df["AST"]
    df["BLK+STL"] = df["BLK"] + df["STL"]
    df["FANTASY"] = (
        df["PTS"]
        + 1.2 * df["REB"]
        + 1.5 * df["AST"]
        + 3 * df["BLK"]
        + 3 * df["STL"]
        - df["TOV"]
    )

    # fix date formatting
    df["DATE"] = pd.to_datetime(df["GAME_DATE"]).dt.date

    # filter to selected player
    dpp = dp[dp.Name == player_name]

    def categorize(row):
        if row["Stat"] == "Points":
            return "PTS"
        elif row["Stat"] == "Dunks":
            return "BLKA"
        elif row["Stat"] == "Minutes Played":
            return "MIN"
        elif row["Stat"] == "Points In First 6 Minutes":
            return "BLKA"
        elif row["Stat"] == "FG Attempted":
            return "FGA"
        elif row["Stat"] == "FG Made":
            return "FGM"
        elif row["Stat"] == "Personal Fouls":
            return "PF"
        elif row["Stat"] == "Rebounds":
            return "REB"
        elif row["Stat"] == "Assists":
            return "AST"
        elif row["Stat"] == "Pts+Rebs+Asts":
            return "PTS+REBS+ASTS"
        elif row["Stat"] == "Fantasy Score":
            return "FANTASY"
        elif row["Stat"] == "3-PT Made":
            return "FG3M"
        elif row["Stat"] == "3-PT Attempted":
            return "FG3A"
        elif row["Stat"] == "Pts+Rebs":
            return "PTS+REBS"
        elif row["Stat"] == "Pts+Asts":
            return "PTS+ASTS"
        elif row["Stat"] == "Rebs+Asts":
            return "REBS+ASTS"
        elif row["Stat"] == "Free Throws Made":
            return "FTM"
        elif row["Stat"] == "Blks+Stls":
            return "BLK+STL"
        elif row["Stat"] == "Blocked Shots":
            return "BLK"
        elif row["Stat"] == "Steals":
            return "STL"
        elif row["Stat"] == "Turnovers":
            return "TOV"
        KeyError

    dpp["NBA_Stat"] = dpp.apply(lambda row: categorize(row), axis=1)

    # compare player to line if applicable
    for i, j in zip(dpp.NBA_Stat, dpp.Line):
        player_names.append(player_name)
        player_stats.append(i)
        player_lines.append(j)

        # OVER
        df["OVER_" + i] = np.where(df[i] > j, 1, 0)

        # calculate probabilty of OVER for each stat for season
        season_prob = np.round(100 * (df["OVER_" + i].sum() / df["OVER_" + i].size), 1)
        # print(player_name, "OVER", i, j, 'SEASON', season_prob)
        season_overs.append(season_prob)
        # same for last 10 games
        last_10_prob = np.round(
            100 * (df.iloc[:10]["OVER_" + i].sum() / df.iloc[:10]["OVER_" + i].size), 1
        )
        # print(player_name, "OVER", i, j, "LAST_10_G", last_10_prob)
        L10_overs.append(last_10_prob)
        # same for last 2 weeks
        last_2W_prob = np.round(
            100
            * (
                df[df.DATE >= (date.today() - timedelta(14))]["OVER_" + i].sum()
                / df[df.DATE >= (date.today() - timedelta(14))]["OVER_" + i].size
            ),
            1,
        )
        # print(player_name, "OVER", i, j, "LAST_2_WK", last_2W_prob)
        L2W_overs.append(last_2W_prob)

        # repeat for UNDER
        df["UNDER_" + i] = np.where(df[i] < j, 1, 0)
        # calculate probabilty of OVER for each stat for season
        season_prob = np.round(
            100 * (df["UNDER_" + i].sum() / df["UNDER_" + i].size), 1
        )
        # print(player_name, "UNDER", i, j, 'SEASON', season_prob)
        season_unders.append(season_prob)
        # same for last 10 games
        last_10_prob = np.round(
            100 * (df.iloc[:10]["UNDER_" + i].sum() / df.iloc[:10]["UNDER_" + i].size),
            1,
        )
        # print(player_name, "UNDER", i, j, "LAST_10_G", last_10_prob)
        L10_unders.append(last_10_prob)
        # same for last 2 weeks
        last_2W_prob = np.round(
            100
            * (
                df[df.DATE >= (date.today() - timedelta(14))]["UNDER_" + i].sum()
                / df[df.DATE >= (date.today() - timedelta(14))]["UNDER_" + i].size
            ),
            1,
        )
        # print(player_name, "UNDER", i, j, "LAST_2_WK", last_2W_prob)
        L2W_unders.append(last_2W_prob)

    time.sleep(0.600)

df2 = pd.DataFrame(
    {
        "Name": player_names,
        "Stat": player_stats,
        "Line": player_lines,
        "season_pct_over": season_overs,
        "L10_pct_over": L10_overs,
        "L2W_pct_over": L2W_overs,
        "season_pct_under": season_unders,
        "L10_pct_under": L10_unders,
        "L2W_pct_under": L2W_unders,
    }
)

print(df2)

df2 = df2[df2["Stat"] != "BLKA"]

df2.to_csv(r"./PrizePicks/Datasets/" + timestr + "_probs.csv", index=False)
