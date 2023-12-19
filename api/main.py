from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    df = pd.read_csv("api/static/sessions.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    result_dict = {}
    for index, row in df.iterrows():
        start_time_key = row['start_time'].strftime("%-I %p")

        if row['start_time'] <= datetime.now() <= row['end_time']:
                if start_time_key not in result_dict:
                    result_dict[start_time_key] = []

                row_dict = row.to_dict()
                row_dict['index'] = index
                result_dict[start_time_key].append(row_dict)

    result_dict = {key: value for key, value in result_dict.items() if
                   value[0]["start_time"] <= datetime.now() <= value[0]["end_time"]}
    return render_template('index.html', sessions=result_dict)


@app.route('/<timeframe>', methods=['GET', 'POST'])
def filter_by_day(timeframe):
    df = pd.read_csv("api/static/sessions.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df = df[df['start_time'].dt.day_name() == timeframe.title()]
    result_dict = {}

    for index, row in df.iterrows():
        start_time_key = row['start_time'].strftime("%-I %p")
        if start_time_key not in result_dict:
            result_dict[start_time_key] = []

        row_dict = row.to_dict()
        row_dict['index'] = index
        result_dict[start_time_key].append(row_dict)

    return render_template('filter_by_day.html', sessions=result_dict, timeframe=timeframe)

@app.route('/filter/<track>')
def filter_now(track):
    print(f"Received track: {track}")
    df = pd.read_csv("api/static/sessions.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    result_dict = {}
    for index, row in df.iterrows():
        start_time_key = row['start_time'].strftime("%-I %p")

        if row['start_time'] <= datetime.now() <= row['end_time']:
            if start_time_key not in result_dict:
                result_dict[start_time_key] = []

            row_dict = row.to_dict()
            row_dict['index'] = index
            result_dict[start_time_key].append(row_dict)

    result_dict = {key: value for key, value in result_dict.items() if
                   value[0]["start_time"] <= datetime.now() <= value[0]["end_time"]}

    filtered_dict = {key: value for key, value in result_dict.items() if value[0]["track"] == track}
    return render_template('index.html')

@app.route('/filter/<timeframe>/<track>')
def filter(timeframe, track):
    df = pd.read_csv("api/static/sessions.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df = df[df['start_time'].dt.day_name() == timeframe.title()]
    result_dict = {}
    for index, row in df.iterrows():
        start_time_key = row['start_time'].strftime("%-I %p")
        if start_time_key not in result_dict:
            result_dict[start_time_key] = []

        row_dict = row.to_dict()
        row_dict['index'] = index
        result_dict[start_time_key].append(row_dict)

    filtered_dict = {key: value for key, value in result_dict.items() if value[0]["track"] == track}

    return render_template('filter_by_day.html', sessions=filtered_dict)


@app.route('/session/<index>')
def session(index):
    index = int(index)

    df = pd.read_csv("api/static/sessions.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    session_data = df.loc[index].to_dict()

    return render_template('session.html', session=session_data)

@app.route('/presenter/<name>')
def presenter(name):
    df = pd.read_csv("api/static/sessions.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    presenter_row = df.loc[df['presenter'] == name].to_dict('records')[0]

    return render_template('presenter.html', presenter=presenter_row)

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/exhibitors')
def exhibitors():
    df = pd.read_csv("api/static/exhibitors.csv").to_dict('records')
    return render_template('exhibitors.html', exhibitors=df)

@app.route('/exhibitor_page/<name>')
def exhibitor_page(name):
    df = pd.read_csv("api/static/exhibitors.csv")
    row = df.loc[df['name'] == name].to_dict('records')[0]
    return render_template('exhibitor_page.html', exhibitor=row)


if __name__ == '__main__':
    app.run(debug=True)
