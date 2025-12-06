import requests
import csv
import datetime
import os

# Define the station and output CSV file
STATION = "KOJC"
CSV_FILE = "today_precipitation_data.csv"

def fetch_today():
    url = "https://data.rcc-acis.org/StnData"
    
    # Today's date
    today = datetime.date.today().strftime("%Y-%m-%d")

    print(f"Fetching today's totals for: {today}")

    new_rows = []

    payload = {
        "sid": STATION,
        "sdate": today,
        "edate": today,
        "elems": [{"name": "pcpn", "interval": "dly"}]
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Expecting exactly one result for "today"
        if 'data' in data and len(data['data']) > 0:
            entry = data['data'][0]
            date_str = entry[0]
            raw_precip = entry[1]

            # Clean data
            if raw_precip == "T":
                precip_val = 0.001
            elif raw_precip == "M" or raw_precip == "S":
                precip_val = 0.0
            else:
                try:
                    precip_val = float(raw_precip)
                except ValueError:
                    precip_val = 0.0
            
            print(f"  - {STATION}: {precip_val} in")
            new_rows.append([date_str, STATION, precip_val])
        else:
            print(f"  - {STATION}: No data found for today.")

    except Exception as e:
        print(f"  - {STATION}: Error {e}")

    # Append to CSV if we found data
    if new_rows:
        # Check if file exists to know if we need a header
        file_exists = os.path.isfile(CSV_FILE)
        
        with open(CSV_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["date", "station_id", "precip_in"])
            writer.writerows(new_rows)
        print("Success: Data appended to CSV.")

if __name__ == "__main__":
    fetch_today()
