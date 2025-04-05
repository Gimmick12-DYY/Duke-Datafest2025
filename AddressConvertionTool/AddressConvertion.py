import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep

# Load the original CSV file
df = pd.read_csv('/Users/mac/Duke-Datafest2025/Dataset/Leases.csv')

# Select only the relevant columns
df_filtered = df[['address', 'city', 'state']]

# Save the new CSV
output_path = '/Users/mac/Duke-Datafest2025/AddressConvertionTool/AddressSheet.csv'
df_filtered.to_csv(output_path, index=False)

# Read the filtered address sheet
df = pd.read_csv(output_path)

# Combine address parts into a full string
df['full_address'] = df['address'] + ', ' + df['city'] + ', ' + df['state']

# Set up OpenStreetMap Nominatim geocoder with a valid user agent
geolocator = Nominatim(user_agent="address_converter")

# Geocoding function
def geocode(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return pd.Series([location.latitude, location.longitude])
    except:
        pass
    return pd.Series([None, None])

# Loop through addresses and collect coordinates
latitudes = []
longitudes = []

for addr in df['full_address']:
    print(f"Geocoding: {addr}")
    lat, lon = geocode(addr)
    latitudes.append(lat)
    longitudes.append(lon)
    sleep(1)  # Respect Nominatim usage policy

# Add lat/lon to DataFrame
df['latitude'] = latitudes
df['longitude'] = longitudes

# Drop the full address column
df = df.drop(columns=['full_address'])

# Save result to CSV
df.to_csv('/Users/mac/Duke-Datafest2025/AddressConvertionTool/AddressSheet_with_coords.csv', index=False)
print("✅ Done! File saved as AddressSheet_with_coords.csv")
