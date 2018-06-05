
import sys
import json
import csv 

data = {}
geojson = {}

## Step 1: Load the labor force data set, and store into a dictionary
## based on the state and county codes
with open('labor-force.csv', 'r') as f:
  reader = csv.DictReader(f)
  for row in reader:
    statefip = int(row['state_fips'])
    countyfip = int(row['county_fips'])
    labor_force = int(row['labor_force'])
    employed = int(row['employed'])
    unemployment_level = int(row['unemployment_level'])
    unemployment_rate = float(row['unemployment_rate'])

    if statefip not in data:
        data[statefip] = {}
    data[statefip][countyfip] = {
      'labor_force': labor_force,
      'employed': employed,
      'unemployment_level': unemployment_level,
      'unemployment_rate': unemployment_rate
    }

## Step 2: Load the shapes for the counties (features), lookup the labor force
## values based on the state/county codes, and set it as part of the feature
## properties
with open('counties.json', 'r') as f:
  geojson = json.load(f)
  for feature in geojson['features']:
    featureProperties = feature['properties']
    statefp = int(featureProperties['STATEFP'])
    countyfp = int(featureProperties['COUNTYFP'])
    featureData = data.get(statefp).get(countyfp, {})
    for key in featureData.keys():
      featureProperties[key] = featureData[key]

## Step 3: Save the augmented shapefile
with open('counties-unemployment.geojson', 'w') as f:
  json.dump(geojson, f)
