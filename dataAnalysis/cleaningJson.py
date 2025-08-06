import pandas as pd
import numpy as np
import json


#combines json files into one dataframe
def combine(files):
    frames = process(files)
    result = pd.concat(frames)
    print("jsons combined")
    return result

#helper function for processing json data
#loads jsons and takes the necessary data
def process(files):
    frames = []
    for file in files:
        with open(file) as train_file:
            dict_train = json.load(train_file)

        data = pd.json_normalize(dict_train)
        df = data[['address.streetAddress', 'address.city', 'address.zipcode', 'resoFacts.yearBuilt', 'resoFacts.livingArea', 'resoFacts.cooling', 'resoFacts.heating']]
        frames.append(df)
    return frames

#renames columns and converts data to optimal format
def clean(data):
    data = pd.DataFrame(data)
    data = data.rename(columns={"address.streetAddress": "streetAddress" , "address.city": "City", 
                     "address.zipcode": "Zipcode", "resoFacts.yearBuilt": "yearBuilt", "resoFacts.livingArea": "squareFootage", 
                     "resoFacts.cooling": "coolingMethod", "resoFacts.heating": "heatingMethod"})
    
    data["homeAge"] = 2025 - data["yearBuilt"] 

   

    data['squareFootage'] = data['squareFootage'].str.replace(" sqft", '')
    data['squareFootage'] = data['squareFootage'].str.replace(',', '')

    data["coolingMethod"] = data["coolingMethod"].astype(str)
    data["heatingMethod"] = data["heatingMethod"].astype(str)
    data['coolingMethod'] = data['coolingMethod'].replace({"[]": ""})
    data['coolingMethod'] = data['coolingMethod'].replace({"None": ""})

    data['coolingMethod'] = data['coolingMethod'].replace("", np.nan)
    data['heatingMethod'] = data['heatingMethod'].replace({"[]": ""})
    data['heatingMethod'] = data['heatingMethod'].replace({"None": ""})
    data['heatingMethod'] = data['heatingMethod'].replace("", np.nan)
    data['squareFootage'] = data['squareFootage'].replace("", np.nan)

    data = data.dropna(subset='heatingMethod')
    data = data.dropna(subset='coolingMethod')
    data = data.dropna(subset='squareFootage')
    #print(data.head)
    return data




# if __name__ == "__main__": 
#     files = [file1, file2, file3, file4, file5]
#     data = combine(files)
#     cleaned_data = clean(data)
#     cleaned_data.to_csv()
    




