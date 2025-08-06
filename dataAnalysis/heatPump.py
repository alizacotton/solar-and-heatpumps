from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

from dataAnalysis.env.env import PATH

#automates opening a web browser and grabs information from heat pump calculator
def scrape(squareft, heat, cool):
    chromeService = webdriver.ChromeService(executable_path = PATH)
    driver = webdriver.Chrome(service = chromeService)

    driver.get("https://heatpumpshooray.com/#calculator")
    zip = driver.find_element(By.NAME, "zip-text-input")
    zip.send_keys("05445")

    sqft = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/input')

    sqft.send_keys(Keys.ARROW_RIGHT)
    sqft.send_keys(Keys.ARROW_RIGHT)
    sqft.send_keys(Keys.ARROW_RIGHT)
    sqft.send_keys(Keys.ARROW_RIGHT)
    sqft.send_keys(Keys.BACK_SPACE)
    sqft.send_keys(Keys.BACK_SPACE)
    sqft.send_keys(Keys.BACK_SPACE)
    sqft.send_keys(Keys.BACK_SPACE)
    sqft.send_keys(squareft)

    status = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/label')
    while status.text == "Unknown":
        zip = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[1]/div[1]/div[2]/div[1]/input')
        zip.send_keys(Keys.BACK_SPACE)
        zip.send_keys(Keys.BACK_SPACE)
        zip.send_keys(Keys.BACK_SPACE)
        zip.send_keys(Keys.BACK_SPACE)
        zip.send_keys(Keys.BACK_SPACE)
        zip.send_keys("05445")


    select = Select(driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[2]/div[1]/div[2]/div/div/div/select'))
    if heat == "Oil":
        select.select_by_visible_text("Fuel Oil")
    if heat == "Electric":
        select.select_by_visible_text("Electricity")
    if heat == "Propane":
        select.select_by_visible_text("Propane")
    if heat == "Gas":
        select.select_by_visible_text("Natural Gas")



    if cool == "['None']":
        button = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[3]/div[1]/div[2]/div/div/label/div/div[2]/div')
        button.click()

    button = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[4]/button')
    button.click()


    try:
        main = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div[3]/code'))
        )

        lifetimeFuelCost = main.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div[3]/code')

        heatPumpName = main.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[6]/div/div/div[3]/div/div/div[1]/div/h2')

        heatLoadCoverage = main.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[6]/div/div/div[3]/div/div/div[2]/div[2]/div[1]/code[5]')

        coolingLoadCoverage = main.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[6]/div/div/div[3]/div/div/div[2]/div[2]/div[1]/code[6]')

        carbonSaved = main.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[6]/div/div/div[2]/div/div[1]/h2')

        unitCost = main.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div[6]/code')

        installationCost = main.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[5]/div/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div[9]/code')

        result = {
            'lifetimeFuelCost': lifetimeFuelCost.text,
            'heatPumpName': heatPumpName.text,
            'heatLoadCoverage': heatLoadCoverage.text,
            'coolingLoadCoverage': coolingLoadCoverage.text,
            'carbonSaved': carbonSaved.text,
            'unitCost': unitCost.text,
            'installationCost': installationCost.text
        }

        print(result)
        driver.quit()
        return result


    except:
        driver.quit()
        return 1
    
#use this function to apply the scraped data into your datatable
def apply_heat_pump_data(row):
    print("working")
    print(row['streetAddress'])
    column_name1 = 'squareFootage'
    column_name2 = 'heatingMethod'
    column_name3 = 'coolingMethod'
    squareft_value = row[column_name1]
    heat_value = clean_heat(row[column_name2])
    cool_value = row[column_name3]
    if heat_value == "Heat Pump":
        pass
    if heat_value == None:
        pass
    else: 
        d = scrape(squareft_value, heat_value, cool_value)
        if d == 1:
            return row
        else: 
            row['lifetimeFuelCost'] = d['lifetimeFuelCost']
            row['heatPumpName'] = d['heatPumpName']
            row['heatLoadCoverage'] = d['heatLoadCoverage']
            row['coolingLoadCoverage'] = d['coolingLoadCoverage']
            row['carbonSaved'] = d['carbonSaved']
            row['unitCost'] = d['unitCost']
            row['installationCost'] = d['installationCost']
            return row
        
#helper function to select a heating method for the calculator
def clean_heat(heat_method):
    if heat_method == None:
        return None
    x = ""
    if "Oil" in heat_method:
        x = "Oil"
        print("oil")
    if "Heat Pump" in heat_method:
        x = "Heat Pump"
        print("heatpump")
    if "Heat pump" in heat_method:
        x = "Heat Pump"
        print("heatpump")
    if "Propane" in heat_method:
        x = "Propane"
        print("propane")
    if "Gas" in heat_method:
        x = "Gas"
        print("gas")
    if "Electric" in heat_method:
        x = "Electric"
        print("electric")
    if "Radiant" in heat_method:
        x = "Electric"
        print("electric")
    if "Other" in heat_method:
        x = "Electric"
        print("electric")
    if "Hot Water" in heat_method:
        x = "Oil"
        print("oil")
    if "Wood" in heat_method:
        x = "Oil"
        print("oil")
    if "Pellet Stove" in heat_method:
        x = "Oil"
        print("oil")
    if "Radiator" in heat_method:
        x = "Oil"
        print("oil")
    if "Baseboard" in heat_method:
        x = "Electric"
        print("electric")
    if "Hot Air" in heat_method:
        x = "Gas"
        print("gas")
    if "Forced Air" in heat_method:
        x = "Electric"
        print("electric")
    if "Forced air" in heat_method:
        x = "Electric"
        print("electric")
    return x

#calculates power needed for the heat pump based on fuel costs
#apply to data table using apply
def calculate_power(row):
    row['lifetimeFuelCost'] = str(row['lifetimeFuelCost']).replace('$', '')
    row['lifetimeFuelCost'] = str(row['lifetimeFuelCost']).replace(',', '')
    if row['lifetimeFuelCost'] == None:
        row['lifetimeFuelCost'] = "already has heatpump"
    row['heatPumpKwhPerYear'] = (((float(row['lifetimeFuelCost'])) / 15) / .21)
    return row
    
def clean(row):
    heat_method = row['heatingMethod']
    y = clean_heat(heat_method)
    row['heat'] = y
    return row
    
   



#if __name__ == "__main__":
    #load data
    # df = pd.read_csv() 
    # df = df.apply(apply_heat_pump_data, axis = 1)
    # df = df.apply(calculate_power, axis = 1)
    # print(df.head)
    # filepath = ""
    # df.to_csv(filepath, index=False)
   
