from flask import Flask, render_template, request
import pandas as pd
from urllib.parse import unquote
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    df = pd.read_csv("api/static/oblc_data - sessions.csv")
    presenter_df = pd.read_csv("api/static/oblc_data - presenters.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    result_dict = {}

    for index, row in df.iterrows():
        start_time_key = row['start_time'].strftime("%-l:%M %p")
        end_time_key = row['end_time'].strftime("%-l:%M %p")
        time_range_key = f"{start_time_key} - {end_time_key}"

        if time_range_key not in result_dict:
            result_dict[time_range_key] = []

        presenter_value = row['presenter']
        presenter_list = [] if pd.isna(presenter_value) else presenter_value.split(', ')

        row_dict = row.to_dict()
        row_dict['index'] = index
        row_dict['presenters_list'] = presenter_list
        result_dict[time_range_key].append(row_dict)

    result_dict = {key: value for key, value in result_dict.items() if
                   value[0]["start_time"] <= datetime.now() <= value[0]["end_time"]}
    return render_template('index.html', sessions=result_dict, presenters=presenter_df)


@app.route('/<timeframe>', methods=['GET', 'POST'])
def filter_by_day(timeframe):
    df = pd.read_csv("api/static/oblc_data - sessions.csv")
    presenter_df = pd.read_csv("api/static/oblc_data - presenters.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    df = df[df['start_time'].dt.day_name() == timeframe.title()]
    result_dict = {}

    for index, row in df.iterrows():
        start_time_key = row['start_time'].strftime("%-l:%M %p")
        end_time_key = row['end_time'].strftime("%-l:%M %p")
        time_range_key = f"{start_time_key} - {end_time_key}"

        if time_range_key not in result_dict:
            result_dict[time_range_key] = []

        presenter_value = row['presenter']
        presenter_list = [] if pd.isna(presenter_value) else presenter_value.split(', ')

        row_dict = row.to_dict()
        row_dict['index'] = index
        row_dict['presenters_list'] = presenter_list
        result_dict[time_range_key].append(row_dict)

    return render_template('filter_by_day.html', sessions=result_dict, presenters=presenter_df, timeframe=timeframe)

@app.route('/session/<index>')
def session(index):
    index = int(index)
    presenter_df = pd.read_csv("api/static/oblc_data - presenters.csv")
    df = pd.read_csv("api/static/oblc_data - sessions.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    session_data = df.loc[index].to_dict()

    # Split the presenter list
    if 'presenter' in session_data and isinstance(session_data['presenter'], str):
        session_data['presenter_list'] = session_data['presenter'].split(', ')
    else:
        session_data['presenter_list'] = []

    return render_template('session.html', presenters=presenter_df, session=session_data)


@app.route('/presenter/<name>')
def presenter(name):
    decoded_name = unquote(name)
    df = pd.read_csv("api/static/oblc_data - presenters.csv")

    presenter_row = df.loc[df['presenter'] == decoded_name].to_dict('records')[0]

    return render_template('presenter.html', presenter=presenter_row)

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/sessions')
def sessions():
    df = pd.read_csv("api/static/summaries.csv").to_dict('records')
    return render_template('sessions.html', sessions=df)

@app.route('/sponsors')
def sponsors():
    df = pd.read_csv("api/static/exhibitors.csv").to_dict('records')
    return render_template('sponsors.html', sponsors=df)

@app.route('/sponsor_page/<name>')
def sponsor(name):
    decoded_name = unquote(name)
    df = pd.read_csv("api/static/exhibitors.csv")
    row = df.loc[df['name'] == decoded_name].to_dict('records')[0]
    return render_template('sponsor_page.html', sponsor=row)


if __name__ == '__main__':
    app.run(debug=True)
