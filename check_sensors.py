import json
import pandas as pd

def get_overdue_sensors(threshold):
    # Les inn sensorinfo fra regnearket.
    temp = pd.read_excel("sensors.xlsx")
    Tempxlsx = []
    for xlsx_row in temp.itertuples():
        Tempxlsx.append(list(xlsx_row))

    # Les inn hvor mange dager siden siste kalibrering.
    with open("calibrations.csv", "r") as calfile:
        Tempcal = []
        for cal_line in calfile:
            Tempcal.append(cal_line.strip().split(","))

    # Koble hver sensor til kalibreringsdataene ved hjelp av sensor-ID.
    Tempres = []
    for sensor_line in Tempxlsx:
        sensor_id = sensor_line[1]
        lab = sensor_line[2]
        owner = sensor_line[3]
        for cal_data in Tempcal[1:]:
            if sensor_id == cal_data[0]:
                Tempres.append([sensor_id, lab, owner, cal_data[1]])
                break

    # Ta bare med sensorer som har overskredet den konfigurerte grensen.
    result = []
    for matched_data in Tempres:
        sensor_id = matched_data[0]
        lab = matched_data[1]
        owner = matched_data[2]
        days_since_calibration = int(matched_data[3])
        if days_since_calibration > threshold:
            result.append({
                "sensor_id": sensor_id,
                "lab": lab,
                "owner": owner,
                "days_since_calibration": days_since_calibration
            })

    return result


# Les grenseverdien og filnavnet for resultatet fra konfigurasjonen.
with open("config.yml", "r") as infile:
    config = {}
    for line in infile:
        key, value = line.strip().split(":", 1)
        config[key] = value.strip().strip('"')

threshold = int(config["max_days_since_calibration"])
overdue_sensors = get_overdue_sensors(threshold)
# Skriver sensorene som en JSON-liste.
with open(config["output_file"], "w") as outfile:
    json.dump(overdue_sensors, outfile, indent=2)