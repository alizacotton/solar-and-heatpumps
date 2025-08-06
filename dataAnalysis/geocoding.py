import requests
import pandas as pd
from dataAnalysis.env.env import API_KEY

geo_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

#calls api on address
def get_coordinate_data(address):
    #print(address)
    params = {
        'key': API_KEY,
        'address': address
    }
    response = requests.get(geo_url, params=params).json()
    if response['status'] == 'OK':
        latitude = response['results'][0]['geometry']['location']['lat']
        longitude = response['results'][0]['geometry']['location']['lng']
        return latitude, longitude 
    else:
        return 1

#use this function with the apply method to iterate over rows and
#store api call within your dataframe
def apply_coordinate_data(row):
    row['Address'] = row['streetAddress'] + " " + row['City'] + ", VT"
    column_name = 'Address'
    address_value = row[column_name]
    #print(address_value)
    address_lat, address_lng = get_coordinate_data(address_value)
    row['lat'] = address_lat
    row['lng'] = address_lng
    return row



# if __name__ == "__main__":
#     df = pd.read_csv()
#     df = df.apply(apply_coordinate_data, axis = 1)
#     print(df.head)
#     filepath =
#     df.to_csv(filepath, index=False)
    