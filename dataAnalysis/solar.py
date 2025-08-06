import requests
import pandas as pd
import json
import csv

from dataAnalysis.env.env import API_KEY

solar_url = 'https://solar.googleapis.com/v1/buildingInsights:findClosest?'

#gets solar data with and without extra load of heat pump
def extract_data(lat, lng, sqft, heat_adjustment):
   
    params = {
        'location.latitude': lat,
        'location.longitude': lng,
        'requiredQuality': 'MEDIUM',
        'key': API_KEY
    }
    response = requests.get(solar_url, params=params)
    if response.status_code not in range(200, 299):
        return None
    

    try: 
        response = response.json()
        #response = json.loads(response)
        #print(response)
        numPanels = response['solarPotential']['maxArrayPanelsCount']
        #panelCapacityWatts
        totalCapacity = response['solarPotential']['panelCapacityWatts'] * numPanels
        #carbonOffsetFactorKgPerMwh
        carbonOffsetFactorKgPerMwh = response['solarPotential']['carbonOffsetFactorKgPerMwh']
        totalCarbonSaved = carbonOffsetFactorKgPerMwh * totalCapacity

        index = get_bill_index(sqft, 0)
    

        #financial data
        #assuming 150 as avg energy bill
        assumedMonthlyBill = response['solarPotential']['financialAnalyses'][index]['monthlyBill']['units']
        print(assumedMonthlyBill)
        averageKwhPerMonth = response['solarPotential']['financialAnalyses'][index]['averageKwhPerMonth']

        panelConfigIndex = response['solarPotential']['financialAnalyses'][index]['panelConfigIndex']
        #assumed number of panels based on energy consumption
        panelsCount = response['solarPotential']['solarPanelConfigs'][panelConfigIndex]['panelsCount']
        #assumed yearly energy production
        yearlyEnergyDcKwh = response['solarPotential']['solarPanelConfigs'][panelConfigIndex]['yearlyEnergyDcKwh']

        initialAcKwhPerYear = response['solarPotential']['financialAnalyses'][index]['financialDetails']['initialAcKwhPerYear']
        costOfElectricityWithoutSolar = response['solarPotential']['financialAnalyses'][index]['financialDetails']['costOfElectricityWithoutSolar']['units']
        percentPowerFromSolar = response['solarPotential']['financialAnalyses'][index]['financialDetails']['solarPercentage']
        #leasing
        annualLeasingCost = response['solarPotential']['financialAnalyses'][index]['leasingSavings']['annualLeasingCost']['units']
        leasingSavingsYear1 = response['solarPotential']['financialAnalyses'][index]['leasingSavings']['savings']['savingsYear1']['units']
        leasingSavingsYear20 = response['solarPotential']['financialAnalyses'][index]['leasingSavings']['savings']['savingsYear20']['units']
        leasingPresentValueOfSavingsYear20 = response['solarPotential']['financialAnalyses'][index]['leasingSavings']['savings']['presentValueOfSavingsYear20']['units']
        #cash purchase
        upfrontCost = response['solarPotential']['financialAnalyses'][index]['cashPurchaseSavings']['upfrontCost']['units'] #includes tax savings
        rebateValue = response['solarPotential']['financialAnalyses'][index]['cashPurchaseSavings']['rebateValue']['units']
        cashSavingsYear1 = response['solarPotential']['financialAnalyses'][index]['cashPurchaseSavings']['savings']['savingsYear1']['units']
        cashSavingsYear20 = response['solarPotential']['financialAnalyses'][index]['cashPurchaseSavings']['savings']['savingsYear20']['units']
        cashPresentValueOfSavingsYear20 = response['solarPotential']['financialAnalyses'][index]['cashPurchaseSavings']['savings']['presentValueOfSavingsYear20']['units']
        #financed
        annualLoanPayment = response['solarPotential']['financialAnalyses'][index]['financedPurchaseSavings']['annualLoanPayment']['units']
        #loanRebateValue = response['solarPotential']['financialAnalyses'][13]['financedPurchaseSavings']['rebateValue']['units']
        loanInterestRate = response['solarPotential']['financialAnalyses'][index]['financedPurchaseSavings']['loanInterestRate']
        loanSavingsYear1 = response['solarPotential']['financialAnalyses'][index]['financedPurchaseSavings']['savings']['savingsYear1']['units']
        loanSavingsYear20 = response['solarPotential']['financialAnalyses'][index]['financedPurchaseSavings']['savings']['savingsYear20']['units']
        loanPresentValueOfSavingsYear20= response['solarPotential']['financialAnalyses'][index]['financedPurchaseSavings']['savings']['presentValueOfSavingsYear20']['units']

        index = get_bill_index(sqft, heat_adjustment)

        H_assumedMonthlyBill = response['solarPotential']['financialAnalyses'][index -1]['monthlyBill']['units']
        H_averageKwhPerMonth = response['solarPotential']['financialAnalyses'][index]['averageKwhPerMonth']
        H_panelConfigIndex = response['solarPotential']['financialAnalyses'][index]['panelConfigIndex']
        #assumed number of panels based on energy consumption
        H_panelsCount = response['solarPotential']['solarPanelConfigs'][H_panelConfigIndex]['panelsCount']
        #assumed yearly energy production
        H_yearlyEnergyDcKwh = response['solarPotential']['solarPanelConfigs'][H_panelConfigIndex]['yearlyEnergyDcKwh']
        H_initialAcKwhPerYear = response['solarPotential']['financialAnalyses'][index]['financialDetails']['initialAcKwhPerYear']
        H_costOfElectricityWithoutSolar = response['solarPotential']['financialAnalyses'][index]['financialDetails']['costOfElectricityWithoutSolar']['units']
        H_percentPowerFromSolar = response['solarPotential']['financialAnalyses'][index]['financialDetails']['solarPercentage']
        #leasing
        H_annualLeasingCost = response['solarPotential']['financialAnalyses'][index]['leasingSavings']['annualLeasingCost']['units']
        H_leasingSavingsYear1 = response['solarPotential']['financialAnalyses'][index]['leasingSavings']['savings']['savingsYear1']['units']
        H_leasingSavingsYear20 = response['solarPotential']['financialAnalyses'][index]['leasingSavings']['savings']['savingsYear20']['units']
        H_leasingPresentValueOfSavingsYear20 = response['solarPotential']['financialAnalyses'][index]['leasingSavings']['savings']['presentValueOfSavingsYear20']['units']
        #cash purchase
        H_upfrontCost = response['solarPotential']['financialAnalyses'][index]['cashPurchaseSavings']['upfrontCost']['units'] #includes tax savings
        H_rebateValue = response['solarPotential']['financialAnalyses'][index]['cashPurchaseSavings']['rebateValue']['units']
        H_cashSavingsYear1 = response['solarPotential']['financialAnalyses'][index]['cashPurchaseSavings']['savings']['savingsYear1']['units']
        H_cashSavingsYear20 = response['solarPotential']['financialAnalyses'][index]['cashPurchaseSavings']['savings']['savingsYear20']['units']
        H_cashPresentValueOfSavingsYear20 = response['solarPotential']['financialAnalyses'][index]['cashPurchaseSavings']['savings']['presentValueOfSavingsYear20']['units']
        #financed
        H_annualLoanPayment = response['solarPotential']['financialAnalyses'][index]['financedPurchaseSavings']['annualLoanPayment']['units']
        #loanRebateValue = response['solarPotential']['financialAnalyses'][13]['financedPurchaseSavings']['rebateValue']['units']
        H_loanInterestRate = response['solarPotential']['financialAnalyses'][index]['financedPurchaseSavings']['loanInterestRate']
        H_loanSavingsYear1 = response['solarPotential']['financialAnalyses'][index]['financedPurchaseSavings']['savings']['savingsYear1']['units']
        H_loanSavingsYear20 = response['solarPotential']['financialAnalyses'][index]['financedPurchaseSavings']['savings']['savingsYear20']['units']
        H_loanPresentValueOfSavingsYear20= response['solarPotential']['financialAnalyses'][index]['financedPurchaseSavings']['savings']['presentValueOfSavingsYear20']['units']

        result = {
            'maxPanels': numPanels,
            'maxCapacity': totalCapacity, 
            'maxCarbonSavings': totalCarbonSaved, 
            'assumedMonthlyBill': assumedMonthlyBill,
            'avgKwhPerMonth': averageKwhPerMonth,
            'likelyNumPanels': panelsCount,
            'likelyYearlyEnergyProduction': yearlyEnergyDcKwh,
            'initialAcKwhPerYear': initialAcKwhPerYear,
            'costOfElectricityWithoutSolar': costOfElectricityWithoutSolar,
            'percentPowerFromSolar': percentPowerFromSolar,
            'annualLeasingCost': annualLeasingCost,
            'leasingSavingsYr1': leasingSavingsYear1,
            'leasingSavingsYr20': leasingSavingsYear20, 
            'leasingPresentValueOfSavingsYr20': leasingPresentValueOfSavingsYear20,
            #cash purchase
            'cashUpfrontCost': upfrontCost,
            'cashRebateValue': rebateValue,
            'cashSavingsYr1': cashSavingsYear1,
            'cashSavingsYr20': cashSavingsYear20,
            'cashPresentValueOfSavingsYr20': cashPresentValueOfSavingsYear20,
            #financed
            'annualLoanPayment': annualLoanPayment,
            #print(loanRebateValue) 
            'assumedLoanInterestRate': loanInterestRate,
            'loanSavingsYr1': loanSavingsYear1,
            'loanSavingsYr20': loanSavingsYear20,
            'loanPresentValueOfSavingsYr20': loanPresentValueOfSavingsYear20,

            'H_assumedMonthlyBill': H_assumedMonthlyBill,
            'H_avgKwhPerMonth': H_averageKwhPerMonth,
            'H_likelyNumPanels': H_panelsCount,
            'H_likelyYearlyEnergyProduction': H_yearlyEnergyDcKwh,
            'H_initialAcKwhPerYear': H_initialAcKwhPerYear,
            'H_costOfElectricityWithoutSolar': H_costOfElectricityWithoutSolar,
            'H_percentPowerFromSolar': H_percentPowerFromSolar,
            'H_annualLeasingCost': H_annualLeasingCost,
            'H_leasingSavingsYr1': H_leasingSavingsYear1,
            'H_leasingSavingsYr20': H_leasingSavingsYear20, 
            'H_leasingPresentValueOfSavingsYr20': H_leasingPresentValueOfSavingsYear20,
            #cash purchase
            'H_cashUpfrontCost': H_upfrontCost,
            'H_cashRebateValue': H_rebateValue,
            'H_cashSavingsYr1': H_cashSavingsYear1,
            'H_cashSavingsYr20': H_cashSavingsYear20,
            'H_cashPresentValueOfSavingsYr20': H_cashPresentValueOfSavingsYear20,
            #financed
            'H_annualLoanPayment': H_annualLoanPayment,
            #print(loanRebateValue) 
            'H_assumedLoanInterestRate': H_loanInterestRate,
            'H_loanSavingsYr1': H_loanSavingsYear1,
            'H_loanSavingsYr20': H_loanSavingsYear20,
            'H_loanPresentValueOfSavingsYr20': H_loanPresentValueOfSavingsYear20

        }
        return result
    except:
        print("error")
        pass 


    #return result

#helper function to access correct financial and configuration 
#information based on power usage
def get_bill_index(sqft, adjustment):
    cost = (sqft *.05) + (adjustment * .22)
 
    if cost <= 100:
        index = 11

    if 100 < cost <= 125:
        index = 12

    if 125 < cost <= 150:
        index = 13

    if 150 < cost <= 175:
        index  = 14

    if 175 < cost <= 200:
        index = 15

    if 200 < cost <= 225:
        index = 16

    if 225 < cost <= 250:
        index = 17

    if 250 < cost <= 300:
        index = 18

    if 300 < cost <= 350:
        index = 19

    if 300 < cost <= 350:
        index = 20

    if 350 < cost <= 400:
        index = 21

    if 400 < cost <= 450:
        index = 22

    if cost > 450:
        index = 22

    return index



#adds solar data into datatable
def apply_solar_data(row):
    print(row['streetAddress'])
    column_name1 = 'lat'
    column_name2 = 'lng'
    lat_value = float(row[column_name1])
    lng_value = float(row[column_name2])
    sqft_value = float(row['squareFootage'])
    heat_adjustment = float(row['heatPumpKwhPerYear'])
    d = extract_data(lat_value, lng_value, sqft_value, heat_adjustment)
    if d == None:
        return row
    else: 
        row['maxPanels'] = d['maxPanels']
        row['maxCapacity'] = d['maxCapacity']
        row['maxCarbonSavings'] = d['maxCarbonSavings']
        row['assumedMonthlyBill'] = d['assumedMonthlyBill'] 
        row['averageKwhPerMonth'] = d['avgKwhPerMonth']
        row['likelyNumPanels'] = d['likelyNumPanels']
        row['likelyYearlyEnergyProduction'] = d['likelyYearlyEnergyProduction']
        row['initialAcKwhPerYear'] = d['initialAcKwhPerYear']
        row['costOfElectricityWithoutSolar'] = d['costOfElectricityWithoutSolar']
        row['percentPowerFromSolar'] = d['percentPowerFromSolar']
        row['annualLeasingCost'] = d['annualLeasingCost']
        row['leasingSavingsYr1'] = d['leasingSavingsYr1']
        row['leasingSavingsYr20'] = d['leasingSavingsYr20'] 
        row['leasingPresentValueOfSavingsYr20'] = d['leasingPresentValueOfSavingsYr20']
        #cash purchase
        row['cashUpfrontCost'] = d['cashUpfrontCost']
        row['cashRebateValue'] = d['cashRebateValue']
        row['cashSavingsYr1'] = d['cashSavingsYr1']
        row['cashSavingsYr20'] = d['cashSavingsYr20'] 
        row['cashPresentValueOfSavingsYr20'] = d['cashPresentValueOfSavingsYr20']
        #financed
        row['annualLoanPayment'] = d['annualLoanPayment']
        #print(loanRebateValue) 
        row['assumedLoanInterestRate'] = d['assumedLoanInterestRate']
        row['loanSavingsYr1'] = d['loanSavingsYr1']
        row['loanSavingsYr20'] = d['loanSavingsYr20'] 
        row['loanPresentValueOfSavingsYr20'] = d['loanSavingsYr20']

        #w/ heat pump as added electrical load
        row['H_assumedMonthlyBill'] = d['H_assumedMonthlyBill'] 
        row['H_averageKwhPerMonth'] = d['H_avgKwhPerMonth']
        row['H_likelyNumPanels'] = d['H_likelyNumPanels']
        row['H_likelyYearlyEnergyProduction'] = d['H_likelyYearlyEnergyProduction']
        row['H_initialAcKwhPerYear'] = d['H_initialAcKwhPerYear']
        row['H_costOfElectricityWithoutSolar'] = d['H_costOfElectricityWithoutSolar']
        row['H_percentPowerFromSolar'] = d['H_percentPowerFromSolar']
        row['H_annualLeasingCost'] = d['H_annualLeasingCost']
        row['H_leasingSavingsYr1'] = d['H_leasingSavingsYr1']
        row['H_leasingSavingsYr20'] = d['H_leasingSavingsYr20'] 
        row['H_leasingPresentValueOfSavingsYr20'] = d['H_leasingPresentValueOfSavingsYr20']
        #cash purchase
        row['H_cashUpfrontCost'] = d['H_cashUpfrontCost']
        row['H_cashRebateValue'] = d['H_cashRebateValue']
        row['H_cashSavingsYr1'] = d['H_cashSavingsYr1']
        row['H_cashSavingsYr20'] = d['H_cashSavingsYr20'] 
        row['H_cashPresentValueOfSavingsYr20'] = d['H_cashPresentValueOfSavingsYr20']
        #financed
        row['H_annualLoanPayment'] = d['H_annualLoanPayment']
        #print(loanRebateValue) 
        row['H_assumedLoanInterestRate'] = d['H_assumedLoanInterestRate']
        row['H_loanSavingsYr1'] = d['H_loanSavingsYr1']
        row['H_loanSavingsYr20'] = d['H_loanSavingsYr20'] 
        row['H_loanPresentValueOfSavingsYr20'] = d['H_loanSavingsYr20']
        return row





# if __name__ == "__main__":
#     df = pd.read_csv() 
#     df = df.apply(apply_solar_data, axis = 1)

#     filepath = 
#     df.to_csv(filepath, index=False)
    