from flask import Flask, render_template, request
from app import app, search_objects, get_xls, get_video_url_and_start_time
import xlrd

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/play')
def play():
    videoUrl = "https:d2pipjeqefmgvp.cloudfront.net/" + request.args.get('videoUrl')
    startTime = request.args.get('startTime')
    print("url:", videoUrl)
    print("start:", startTime)
    # You can perform any necessary processing here

    return render_template('templates/play.html', videoUrl=videoUrl, startTime=startTime)

@app.route('/execute_tester', methods=['GET'])
def execute_tester():
    dateString = request.args.get('dateString')
    fileString = request.args.get('fileString')

    if dateString:

        results = search_objects(dateString)
        # Open the Excel file

        xlsFile = get_xls(fileString + "_북한TV편성표.xls")

        wb = xlrd.open_workbook(xlsFile)
        # Select the active worksheet
        ws = wb.sheet_by_index(0)
        # Extract timestamps from the first column (A) and store them in a list
        timestamps = [ws.cell_value(row, 0) for row in range(ws.nrows)]
        # Extract data from the remaining columns (excluding column A)
        data = [[ws.cell_value(row, col) for col in range(1, ws.ncols)] for row in range(ws.nrows)]
        # Pass the timestamps and the entire data to the HTML template
        return render_template('templates/results.html', results=results, dateString=dateString, timestamps=timestamps, data=data, get_video_url_and_start_time=get_video_url_and_start_time)
    else:
        return "Invalid Request: Missing dateString"



if __name__ == '__main__':
    app.run(debug=True)
