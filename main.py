import pandas as pd
from dataAnalysis import combine, process, clean, apply_coordinate_data, apply_heat_pump_data, calculate_power, apply_solar_data
from dataAnalysis import jsonFiles, API_KEY, finalFilepath



if __name__ == "__main__":
    data = combine(jsonFiles)
    data = clean(data)
    data = data.apply(apply_coordinate_data, axis = 1)
    df = data.apply(apply_heat_pump_data, axis = 1)
    df = pd.DataFrame(df)
    df = df.apply(calculate_power, axis = 1)
    df = df.apply(apply_solar_data, axis = 1)
    print(df.head)
    df.to_csv(finalFilepath, index = False) 