import requests
import csv
import datetime
import os

# Same stations as backfill
STATIONS = ["KOJC", "KIXD", "KLWC", "KMCI"]
CSV_FILE = "precipitation_data.csv"  # Path to the CSV file for precipitation data

def fetch_yesterday():
    url = "https://data.rcc-acis.org/StnData"
    
    # ACIS handles "yesterday" keyword automatically, or we can calculate it
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"Fetching daily totals for: {yesterday}")

    new_rows = []

    for station in STATIONS:
        payload = {
            "sid": station,
            "sdate": yesterday,
            "edate": yesterday,
            "elems": [{"name": "pcpn", "interval": "dly"}]
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Expecting exactly one result for "yesterday"
            if 'data' in data and len(data['data']) > 0:
                entry = data['data'][0]
                date_str = entry[0]
                raw_precip = entry[1]

                # Clean data (Same logic as backfill)
                if raw_precip == "T":
                    precip_val = 0.001
                elif raw_precip == "M" or raw_precip == "S":
                    precip_val = 0.0
                else:
                    try:
                        precip_val = float(raw_precip)
                    except ValueError:
                        precip_val = 0.0
                
                print(f"  - {station}: {precip_val} in")
                new_rows.append([date_str, station, precip_val])
            else:
                print(f"  - {station}: No data found for yesterday.")

        except Exception as e:
            print(f"  - {station}: Error {e}")

    # Append to CSV if we found data
    if new_rows:
        # Check if file exists to know if we need a header (in case backfill wasn't run)
        file_exists = os.path.isfile(CSV_FILE)
        
        with open(CSV_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["date", "station_id", "precip_in"])
            writer.writerows(new_rows)
        print("Success: Data appended to CSV.")

if __name__ == "__main__":
    fetch_yesterday()

