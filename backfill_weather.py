import requests
import csv
import datetime

# 1. Configuration
# Closest reliable NOAA/NWS stations to 12601 Pflumm Rd, Overland Park, KS 66213
STATIONS = [
    "KOJC",  # Johnson County Executive Airport (Closest)
    "KIXD",  # New Century AirCenter (Southwest)
    "KLWC",  # Lawrence Municipal Airport (Regional backup)
    "KMCI"   # Kansas City Intl (Major hub, best data continuity)
]

START_DATE = "2025-08-01"
END_DATE = datetime.date.today().strftime("%Y-%m-%d") # Today's date
CSV_FILE = "precipitation_data.csv"

def fetch_history():
    # ACIS API Endpoint (Best for daily summaries)
    url = "https://data.rcc-acis.org/StnData"

    all_rows = []

    print(f"Fetching data from {START_DATE} to {END_DATE}...")

    for station in STATIONS:
        # 2. Build Payload
        payload = {
            "sid": station,
            "sdate": START_DATE,
            "edate": END_DATE,
            "elems": [{"name": "pcpn", "interval": "dly"}]
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # 3. Process Results
            for entry in data.get('data', []):
                date_str = entry[0]
                raw_precip = entry[1]
                
                # 4. Data Cleaning
                if raw_precip == "T": # Trace
                    precip_val = 0.001
                elif raw_precip == "M" or raw_precip == "S": # Missing or Suspect
                    precip_val = 0.0
                else:
                    try:
                        precip_val = float(raw_precip)
                    except ValueError:
                        precip_val = 0.0

                all_rows.append([date_str, station, precip_val])
                
            print(f"  - {station}: Success ({len(data.get('data', []))} days)")

        except Exception as e:
            print(f"  - {station}: Failed ({e})")

    # 5. Write to CSV
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["date", "station_id", "precip_in"]) 
        writer.writerows(all_rows)
    
    print(f"\nDone! Saved to {CSV_FILE}")

if __name__ == "__main__":
    fetch_history()

