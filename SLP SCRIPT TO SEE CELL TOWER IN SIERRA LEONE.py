To see telecom towers in your area (Freetown, Sierra Leone) using Python, we will leverage APIs or datasets that provide geospatial data on telecom towers. 
One such data source is **OpenCelliD**, the largest collaborative community project collecting data about mobile phone towers and cells worldwide. Additionally, you can use **QGIS** or **geopandas** for visualizing the towers on a map.

Here is an approach using OpenCelliD's API to obtain telecom tower data, and **Folium** (a Python library built on Leaflet.js) to visualize the towers on a map.

### Steps:
1. **Register for OpenCelliD API Key**:
   - Visit [OpenCelliD](https://www.opencellid.org/) to sign up and get your **API key**.
   - You'll use this key to query telecom towers data for any location (Freetown or any other area).

2. **Libraries Needed**:
   - `requests`: To query the OpenCelliD API.
   - `pandas`: To process and clean the data.
   - `folium`: To create an interactive map with the telecom towers displayed.

3. **Install Required Libraries**:
   You can install these libraries by running the following commands in your Jupyter Notebook or terminal:
   ```bash
   !pip install requests pandas folium
   ```

4. **Python Code**:

Here is a detailed Python code to fetch telecom tower data from OpenCelliD and visualize it on an interactive map:

```python
import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# OpenCelliD API information
API_KEY = 'YOUR_OPENCELLID_API_KEY'  # Replace with your actual API key

# Define the center of the area (Freetown, Sierra Leone)
latitude = 8.4657  # Latitude of Freetown
longitude = -13.2317  # Longitude of Freetown

# Radius in meters (set this to capture the towers within a given distance)
radius = 10000  # 10 km around the specified point

# OpenCelliD API URL (to fetch cell tower data)
url = f"https://api.opencellid.org/cell/get?key={API_KEY}&lat={latitude}&lon={longitude}&range={radius}"

# Fetch the data from OpenCelliD API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    cell_data = response.json()  # Convert the response to a JSON object
    
    # Load the data into a pandas DataFrame for easy processing
    df = pd.DataFrame(cell_data['cells'])
    
    # Display the first few rows of the dataframe
    print(df.head())
    
    # Create a map centered around Freetown
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    
    # Add a marker cluster layer for better visualization of multiple towers
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add telecom towers to the map as markers
    for index, row in df.iterrows():
        lat = row['lat']
        lon = row['lon']
        radio = row['radio']  # Type of radio (e.g., GSM, LTE)
        cell_id = row['cellid']  # Cell ID of the tower
        tower_info = f"Radio: {radio}, Cell ID: {cell_id}"
        
        # Add marker for each tower
        folium.Marker(location=[lat, lon], 
                      popup=tower_info,
                      icon=folium.Icon(color="blue", icon="info-sign")).add_to(marker_cluster)
    
    # Display the map
    m.save('freetown_telecom_towers.html')
    print("Map saved as 'freetown_telecom_towers.html'. Open it in a browser to view.")
    
else:
    print(f"Failed to fetch data: {response.status_code}")
```

### **Explanation**:

1. **API Call to OpenCelliD**:
   - We make an API request using the **OpenCelliD API** with the parameters `latitude`, `longitude`, and `radius`. This gives us data for telecom towers within the specified radius from Freetown.
   
2. **Process the Data**:
   - The data returned by the API is processed into a pandas DataFrame for easy handling. This data contains the latitude, longitude, cell tower ID, and other information like radio type (GSM, LTE, etc.).
   
3. **Visualization using Folium**:
   - We use **Folium** to create an interactive map. Telecom towers are marked on the map, and a popup for each marker shows the tower's radio type and cell ID.
   
4. **Marker Clustering**:
   - We use the **MarkerCluster** feature to group towers that are close to each other, which makes the map more readable when there are many towers in a small area.
   
5. **Save and View**:
   - The map is saved as an HTML file (`freetown_telecom_towers.html`), which you can open in any web browser to view the telecom towers around Freetown.

### **Extending to Other Areas**:

- You can modify the `latitude` and `longitude` variables to any other location (e.g., another city or country) to fetch and visualize telecom towers for that area. Simply input the desired coordinates.

- You can also adjust the `radius` to extend or limit the search area.

### **How to Run**:

1. Replace `'YOUR_OPENCELLID_API_KEY'` with your actual OpenCelliD API key.
2. Run the script in Jupyter Notebook or any Python IDE.
3. After execution, check for the saved HTML file (`freetown_telecom_towers.html`), and open it in a browser to see the map with telecom towers.

### **Additional Customization**:
- You can filter towers by radio type (GSM, LTE, etc.) if needed.
- You could extend the script to analyze coverage or visualize signal strength (if available in the dataset).



## ADDITIONAL HELP FOR EXTENSION AND MODIFICATION OF SCRIPT TO CAPTURE RADIO TYPE#


 modify the script to include filtering by radio type (e.g., GSM, LTE, etc.) and display additional information like signal strength (if available in the dataset). I'll extend the Python code to allow these options.

### Extended Python Code with Filters for Radio Type and Signal Strength:

```python
import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# OpenCelliD API information
API_KEY = 'YOUR_OPENCELLID_API_KEY'  # Replace with your actual API key

# Define the center of the area (Freetown, Sierra Leone)
latitude = 8.4657  # Latitude of Freetown
longitude = -13.2317  # Longitude of Freetown

# Radius in meters (set this to capture the towers within a given distance)
radius = 10000  # 10 km around the specified point

# OpenCelliD API URL (to fetch cell tower data)
url = f"https://api.opencellid.org/cell/get?key={API_KEY}&lat={latitude}&lon={longitude}&range={radius}"

# Fetch the data from OpenCelliD API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    cell_data = response.json()  # Convert the response to a JSON object
    
    # Load the data into a pandas DataFrame for easy processing
    df = pd.DataFrame(cell_data['cells'])
    
    # Display the first few rows of the dataframe
    print(df.head())
    
    # Create a map centered around Freetown
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    
    # Add a marker cluster layer for better visualization of multiple towers
    marker_cluster = MarkerCluster().add_to(m)
    
    # Set filter options
    # You can modify this to filter by any radio type, e.g., 'GSM', 'LTE', 'UMTS'
    radio_type_filter = ['LTE', 'GSM']  # Filter for LTE and GSM towers
    
    # Optionally, define a minimum signal strength threshold (if available)
    # Set to None if you do not want to filter by signal strength
    min_signal_strength = -90  # Example: filter towers with signal strength above -90 dBm
    
    # Add telecom towers to the map as markers based on the filter criteria
    for index, row in df.iterrows():
        lat = row['lat']
        lon = row['lon']
        radio = row['radio']  # Type of radio (e.g., GSM, LTE)
        cell_id = row['cellid']  # Cell ID of the tower
        signal_strength = row.get('signal', None)  # Signal strength, if available
        
        # Apply filters: check for radio type and signal strength
        if radio in radio_type_filter:
            if min_signal_strength is None or (signal_strength and signal_strength > min_signal_strength):
                # Tower information popup
                tower_info = f"Radio: {radio}, Cell ID: {cell_id}, Signal: {signal_strength} dBm" if signal_strength else f"Radio: {radio}, Cell ID: {cell_id}"
                
                # Add marker for each filtered tower
                folium.Marker(location=[lat, lon], 
                              popup=tower_info,
                              icon=folium.Icon(color="blue", icon="info-sign")).add_to(marker_cluster)
    
    # Display the map
    m.save('filtered_freetown_telecom_towers.html')
    print("Filtered map saved as 'filtered_freetown_telecom_towers.html'. Open it in a browser to view.")
    
else:
    print(f"Failed to fetch data: {response.status_code}")
```

### **Explanation of Modifications**:

1. **Radio Type Filtering**:
   - The variable `radio_type_filter` is a list that defines which types of telecom towers (e.g., `'GSM'`, `'LTE'`, `'UMTS'`) you want to visualize on the map. You can easily modify the list to include any combination of tower types you're interested in.

2. **Signal Strength Filtering**:
   - Signal strength (if available in the dataset) is measured in dBm (decibel-milliwatts), with higher values (closer to 0) indicating a stronger signal. For instance, -60 dBm is stronger than -90 dBm.
   - The variable `min_signal_strength` sets a threshold for displaying towers with signal strength above a certain value (e.g., -90 dBm). If a towers signal strength is better than this threshold, it will be displayed on the map. Set `min_signal_strength = None` to ignore this filter.

3. **Popup Information**:
   - The marker popup now includes both the **radio type** (e.g., LTE or GSM) and the **signal strength** (if available). If signal strength is not available in the data, it will not appear in the popup.

4. **Visualization**:
   - Only the towers that match the filter criteria (radio type and signal strength) will be added to the map.

### **Running the Code**:
- Replace `'YOUR_OPENCELLID_API_KEY'` with your actual OpenCelliD API key.
- Run the script in Jupyter Notebook or any Python IDE.
- After running the code, a filtered map will be saved as an HTML file (`filtered_freetown_telecom_towers.html`). Open it in your browser to view the map with only the filtered telecom towers.

### **Customization**:
- You can change the `radio_type_filter` to any combination of tower types you wish to visualize (e.g., GSM, LTE, etc.).
- Modify the `min_signal_strength` threshold based on the signal quality you want to visualize.
