"""
This project uses nutrinix natural langauge apis to calculate the calories using the inputs that user give about their exercises.
Then it uses Sheety API to store or record users daily exercises and calories into a Google spreadsheet names 'My workout Tracker'
"""

import requests, datetime as dt, os

nutrinix_exercise_endpoint = os.getenv('NUT_EXE_API_URL')
jwt_token_endpoint = os.getenv('NUT_JWT_API_URL')
workout_tracker_api = os.getenv('WOK_TK_API_URL')

#Get JWT to authenticate Nutrinix API
jwt_body = {
    "password": os.getenv('PWD_FOR_JWT'),
    "mobile_number": os.getenv('MOB_FOR_JWT'),
    "email": os.getenv('EMAIL_FOR_JWT')
}

jwt_token_response = requests.post(jwt_token_endpoint, json=jwt_body)
jwt_token = jwt_token_response.json()['x-user-jwt']

#Get user input
user_input = input("Tell me which exercises you did:")

exercise_header = {
    'x-user-jwt': jwt_token
}

query_param = {
    'query': user_input
}

token_param = {
    "Authorization": os.getenv('SHEETY_AUTH_TOKEN')
}

date = dt.datetime.now()
todays_date = date.date().strftime('%d/%m/%Y')
todays_time = date.time().strftime('%H:%M:%S')

#Post query to Nutrinix API to get calorie count
cal_response = requests.post(nutrinix_exercise_endpoint, json=query_param, headers=exercise_header)


for exercise in cal_response.json()["exercises"]:
    exercise_name = exercise['name'].capitalize()
    exercise_duration = exercise['duration_min']
    exercise_calories = exercise['nf_calories']
    exercise_params = {
        "sheet1":
            {
              "date": todays_date,
              "time": todays_time,
              "exercise": exercise_name,
              "duration": exercise_duration,
              "calories": exercise_calories
            }

    }
    #Call Sheety Post API to add row to exisitng workout tracker spreadsheet
    workout_response = requests.post(workout_tracker_api, json=exercise_params, headers=token_param)
    print(workout_response.text)





