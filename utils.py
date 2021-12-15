def get_weather():
    import json
    import requests
    import pandas as pd


    mapquest_url = "http://open.mapquestapi.com/geocoding/v1/address"
    mapquest_api_key = "HxA92vY4cLZuqIg4YeLc90YKnU0UtIpu"

    mapquest_url += "?key="
    mapquest_url += mapquest_api_key
    mapquest_url += "&location=spokane+wa"

    mapquest_response = requests.get(mapquest_url)

    json_obj = json.loads(mapquest_response.text)
    results_obj = json_obj["results"]
    locations_obj = results_obj[0]
    city_locations = locations_obj["locations"]
    coords_list = city_locations[0]["displayLatLng"]

    lat = coords_list["lat"]
    lng = coords_list["lng"]

    #use the lng and lat to find nearest weather station
    meteostat_station_url = "https://meteostat.p.rapidapi.com/stations/nearby"
    station_headers = {
        "x-rapid-host": "meteostat.p.rapidapi.com",
        "x-rapidapi-key": "b998fb38e0msh5bdbc233f355651p1e58ccjsn9224f21113ce"
    }
    query_string = {"lat": lat, "lon": lng}

    station_response = requests.request("GET", meteostat_station_url, headers=station_headers, params=query_string)

    #get station id from station request
    station_obj = json.loads(station_response.text)
    stations_list = station_obj["data"]
    station_id = stations_list[0]["id"]

    #get current date
    meta_data = station_obj["meta"]
    date_time_str = meta_data["generated"]
    date_time_list = date_time_str.split(" ")
    date = date_time_list[0]

    #getting daily weather
    meteostat_daily_url = "https://meteostat.p.rapidapi.com/stations/daily"
    querystring = {"station":station_id,"start":"2021-01-01","end":date,"units":"imperial"}
    headers = {
        'x-rapidapi-host': "meteostat.p.rapidapi.com",
        'x-rapidapi-key': "b998fb38e0msh5bdbc233f355651p1e58ccjsn9224f21113ce"
        }

    #put the dailyh weather data into a df
    daily_response = requests.request("GET", meteostat_daily_url, headers=headers, params=querystring)
    daily_response_obj = json.loads(daily_response.text)
    daily_data_list = daily_response_obj["data"]
    daily_data_df = pd.DataFrame(daily_data_list)
    daily_data_df.set_index("date", inplace=True)

    headers = ["tavg", "tmin", "tmax", "prcp", "snow", "wdir", "wspd", "wpgt", "pres", "tsun"]
    for title in headers:
        missing_sum = 0
        missing_sum = daily_data_df[title].isnull().sum()
        if missing_sum > (len(daily_data_df[title]) * .75):
            daily_data_df.pop(title)
        else:
            for i in range(len(daily_data_df[title])):
                if i == 0:
                    daily_data_df[title].bfill(inplace=True)
                elif i == len(daily_data_df[title]):
                    daily_data_df[title].ffill(inplace=True)
                else:
                    daily_data_df.interpolate()

    return daily_data_df

def get_spotify_df(filename):
    '''
    returns a usable dataframe containing a the spotify data from a JSON file
    Parameter: name of the JSON file containing a users spotify data
    Returns: a Pandas dataframe containing the data
    '''
    import pandas as pd

    stream_hist_df = pd.read_json(filename)

    endtime_unclean_ser = stream_hist_df["endTime"]

    date_list = []
    time_list = []

    for i in range(len(endtime_unclean_ser)):
        curr_string = endtime_unclean_ser[i]
        string_as_list = curr_string.split()

        date = string_as_list[0]
        time = string_as_list[1]

        date_list.append(date)
        time_list.append(time)


    stream_hist_df.pop("endTime")
    stream_hist_df = stream_hist_df.assign(date=date_list)
    stream_hist_df = stream_hist_df.assign(endTime=time_list)

    stream_hist_df.set_index("date", inplace=True)

    return stream_hist_df

def decode_endTime_column(dataframe):
    '''
    decodes the endTime value of each song into an integer between 0 and 24, representing what hour of the day the song was listened to 
    Parameter: dataframe to decod, must have a valid endTime column
    Returns: nothing is returned, but dataframe passed in is updated
    '''

    for i in range(len(dataframe["endTime"])):
        item_list = dataframe["endTime"][i].split(":")
        if item_list[0] == "01":
            dataframe["endTime"][i] = 1
        elif item_list[0] == "02":
            dataframe["endTime"][i] = 2
        elif item_list[0] == "03":
            dataframe["endTime"][i] = 3
        elif item_list[0] == "04":
            dataframe["endTime"][i] = 4
        elif item_list[0] == "05":
            dataframe["endTime"][i] = 5
        elif item_list[0] == "06":
            dataframe["endTime"][i] = 6
        elif item_list[0] == "07":
            dataframe["endTime"][i] = 7
        elif item_list[0] == "08":
            dataframe["endTime"][i] = 8
        elif item_list[0] == "09":
            dataframe["endTime"][i] = 9
        elif item_list[0] == "10":
            dataframe["endTime"][i] = 10
        elif item_list[0] == "11":
            dataframe["endTime"][i] = 11
        elif item_list[0] == "12":
            dataframe["endTime"][i] = 12
        elif item_list[0] == "13":
            dataframe["endTime"][i] = 13
        elif item_list[0] == "14":
            dataframe["endTime"][i] = 14
        elif item_list[0] == "15":
            dataframe["endTime"][i] = 15
        elif item_list[0] == "16":
            dataframe["endTime"][i] = 16
        elif item_list[0] == "17":
            dataframe["endTime"][i] = 17
        elif item_list[0] == "18":
            dataframe["endTime"][i] = 18
        elif item_list[0] == "19":
            dataframe["endTime"][i] = 19
        elif item_list[0] == "20":
            dataframe["endTime"][i] = 20
        elif item_list[0] == "21":
            dataframe["endTime"][i] = 21
        elif item_list[0] == "22":
            dataframe["endTime"][i] = 22
        elif item_list[0] == "23":
            dataframe["endTime"][i] = 23
        elif item_list[0] == "24":
            dataframe["endTime"][i] = 24
        elif item_list[0] == "00":
            dataframe["endTime"][i] = 0

def print_avg_endtime_by_weekday_plot(dataframe, name):
    '''
    
    '''
    import matplotlib.pyplot as plt

    groupedby_day = dataframe.groupby("Day of Week")
    monday = groupedby_day.get_group("Monday")
    tuesday = groupedby_day.get_group("Tuesday")
    wednesday = groupedby_day.get_group("Wednesday")
    thursday = groupedby_day.get_group("Thursday")
    friday = groupedby_day.get_group("Friday")
    saturday = groupedby_day.get_group("Saturday")
    sunday = groupedby_day.get_group("Sunday")

    plt.figure()
    plt.scatter([1, 2, 3, 4, 5, 6, 7], [monday["endTime"].mean(), tuesday["endTime"].mean(), wednesday["endTime"].mean(), thursday["endTime"].mean(), friday["endTime"].mean(), saturday["endTime"].mean(), sunday["endTime"].mean()])
    plt.xticks([1, 2, 3, 4, 5, 6, 7], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    plt.ylabel("Average endTime (hour of day)")
    plt.title(name + " Average endTime by Day of Week")