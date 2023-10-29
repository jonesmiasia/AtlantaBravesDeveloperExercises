from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

data = pd.read_excel(r'static/data/BattedBallData.xlsx')
homeruns = data[data['PLAY_OUTCOME'] == 'HomeRun']


# Batter Leaderboard
def topHomeRuns():
    homerun_counts = homeruns.groupby(['BATTER', 'BATTER_ID']).size().reset_index(name='HOME_RUNS')
    homerun_counts = homerun_counts.sort_values(by='HOME_RUNS', ascending=False)
    homerun_counts = splitName(homerun_counts, 'BATTER')
    return homerun_counts.head(5)


def avgExitSpeed():
    average_exit_speed = data.groupby(['BATTER', 'BATTER_ID'])['EXIT_SPEED'].mean().reset_index()
    average_exit_speed.columns = ['BATTER', 'BATTER_ID', 'AVERAGE_EXIT_SPEED']
    average_exit_speed = average_exit_speed.sort_values(by='AVERAGE_EXIT_SPEED', ascending=False)
    average_exit_speed = splitName(average_exit_speed, 'BATTER')
    return average_exit_speed.head(5)


def sweetSpot():
    sweet_spots = data[(data['LAUNCH_ANGLE'] >= 8) & (data['LAUNCH_ANGLE'] <= 32)]
    sweet_spots_counts = sweet_spots.groupby(['BATTER', 'BATTER_ID']).size().reset_index(name='SWEET_SPOTS')
    sweet_spots_counts = sweet_spots_counts.sort_values(by='SWEET_SPOTS', ascending=False)
    sweet_spots_counts = splitName(sweet_spots_counts, 'BATTER')
    return sweet_spots_counts.head(5)


# Pitcher Leaderboard
def topStrikeouts():
    strikeouts = data[data['PLAY_OUTCOME'] == 'Out']
    strikeouts_counts = strikeouts.groupby(['PITCHER', 'PITCHER_ID']).size().reset_index(name='OUTS')
    strikeouts_counts = strikeouts_counts.sort_values(by='OUTS', ascending=False)
    strikeouts_counts = splitName(strikeouts_counts, 'PITCHER')
    return strikeouts_counts.head(5)


def launchAngleAgainst():
    pitchers = data[data['PITCHER'].notnull()]
    avg_launch_angles = pitchers.groupby('PITCHER')['LAUNCH_ANGLE'].mean()
    sorted_avg_launch_angles = avg_launch_angles.reset_index()
    sorted_avg_launch_angles = splitName(sorted_avg_launch_angles, 'PITCHER')
    unique_pitcher_ids = data[['PITCHER', 'PITCHER_ID']].drop_duplicates()
    sorted_pitchers = sorted_avg_launch_angles.merge(unique_pitcher_ids, on='PITCHER', how='left')
    sorted_pitchers = sorted_pitchers.sort_values(by='LAUNCH_ANGLE', ascending=True)
    return sorted_pitchers.head(5)


# Hang Time vs Distance Plot
def hangTimeVsDistance():
    outcomes = data[data['PLAY_OUTCOME'].isin(['Single', 'Double', 'Triple', 'HomeRun', 'Out'])]
    fig = px.scatter(outcomes, x='HANG_TIME', y='HIT_DISTANCE', color='PLAY_OUTCOME')
    fig.update_layout(legend_title_text='Outcome')
    fig.update_layout(
        xaxis_title='Hang Time (s)',
        yaxis_title='Hit Distance (ft)'
    )
    plot_div_hangtime = fig.to_html(full_html=False)
    return plot_div_hangtime


# Home Run Highlights
def homeRunHighlight(columun_name):
    max = homeruns.loc[homeruns[columun_name].idxmax()]
    max = pd.DataFrame([max])
    max['GAME_DATE'] = max['GAME_DATE'].dt.strftime('%Y-%m-%d')
    max = splitName(max, 'BATTER')
    return max[['FIRST_NAME', 'LAST_NAME', 'BATTER_ID', 'GAME_DATE', columun_name, 'VIDEO_LINK']]


def splitName(df, column_name):
    df[['LAST_NAME', 'FIRST_NAME']] = df[column_name].str.split(', ', expand=True)
    return df


@app.route("/home")
@app.route("/")
def home():
    return render_template(
        "home.html",
        homerun_counts=topHomeRuns(),
        avg_exit_speed=avgExitSpeed(),
        sweet_spots_counts=sweetSpot(),
        strikeouts_counts=topStrikeouts(),
        launch_angle_against=launchAngleAgainst(),
        plot_div_hangtime=hangTimeVsDistance(),
        longest_homerun=homeRunHighlight('HIT_DISTANCE'),
        fastest_homerun=homeRunHighlight('EXIT_SPEED'),
        longest_hangtime_homerun=homeRunHighlight('HANG_TIME'),
        video_link="https://www.mlb.com/player/"
    )


if __name__ == "__main__":
    app.run(debug=True)
