Here's an executable Python code for network analysis to calculate the shortest and fastest time of response and distances from fire stations to points of disasters using PyQGIS. You can execute this in QGIS with the Python console or in a Jupyter notebook with PyQGIS installed.

### Steps:
1. Install the required packages in QGIS or Jupyter Notebook (PyQGIS).
2. Prepare your data: you'll need layers for the fire stations, the road network, and disaster points. Ensure that they are loaded in your QGIS project.
3. The code assumes that your network data includes speed limits or travel times for each road segment.

### PyQGIS Code:

```python
import os
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsNetworkAccessManager, QgsPointXY, 
    QgsCoordinateReferenceSystem, QgsDistanceArea, QgsApplication
)
from qgis.analysis import QgsGraphBuilder, QgsGraphAnalyzer
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsFeature, QgsGeometry

# Initialize the QGIS application (for Jupyter, not necessary in QGIS Python console)
QgsApplication.setPrefixPath("/path/to/your/qgis/installation", True)
qgs = QgsApplication([], False)
qgs.initQgis()

# Load the road network layer and point layers (fire stations, disaster points)
fire_stations_layer = QgsVectorLayer("path_to_fire_stations.shp", "Fire Stations", "ogr")
disaster_points_layer = QgsVectorLayer("path_to_disaster_points.shp", "Disaster Points", "ogr")
road_network_layer = QgsVectorLayer("path_to_road_network.shp", "Road Network", "ogr")

# Ensure layers are valid
if not fire_stations_layer.isValid() or not disaster_points_layer.isValid() or not road_network_layer.isValid():
    print("One or more layers failed to load")
else:
    print("All layers loaded successfully")

# Set up the coordinate reference system
crs = QgsCoordinateReferenceSystem("EPSG:4326")  # WGS 84 CRS

# Calculate distance and shortest path
def calculate_shortest_path(fire_station, disaster_point, road_network_layer):
    builder = QgsGraphBuilder(crs)
    tied_points = []

    # Get features (fire stations and disaster points)
    fire_station_geom = fire_station.geometry().asPoint()
    disaster_geom = disaster_point.geometry().asPoint()

    # Tie the points to the network (find the closest edge)
    tied_fire_station = builder.addVertex(fire_station_geom)
    tied_disaster_point = builder.addVertex(disaster_geom)
    
    tied_points.append(tied_fire_station)
    tied_points.append(tied_disaster_point)

    # Build the graph (road network)
    for feature in road_network_layer.getFeatures():
        geom = feature.geometry()
        length_km = geom.length() / 1000  # Convert to kilometers
        builder.addEdge(geom.vertexAt(0), geom.vertexAt(1), [length_km])

    graph = builder.graph()
    
    # Compute shortest path
    (tree, cost) = QgsGraphAnalyzer.shortestTree(graph, tied_fire_station, 0)

    # Output distance in kilometers
    if cost[tied_disaster_point] == float('inf'):
        print(f"No route found between Fire Station and Disaster Point")
    else:
        print(f"Shortest distance: {cost[tied_disaster_point]} km")
    
    return cost[tied_disaster_point]

# Calculate travel time based on road segment speed
def calculate_fastest_time(fire_station, disaster_point, road_network_layer, average_speed_kmph=50):
    distance = calculate_shortest_path(fire_station, disaster_point, road_network_layer)
    
    # Speed (km/h), Time = Distance / Speed
    time_in_hours = distance / average_speed_kmph
    time_in_minutes = time_in_hours * 60
    
    print(f"Fastest response time: {time_in_minutes:.2f} minutes")
    return time_in_minutes

# Run calculations for all fire stations to disaster points
for fire_station in fire_stations_layer.getFeatures():
    for disaster_point in disaster_points_layer.getFeatures():
        print(f"Calculating for Fire Station ID: {fire_station.id()} and Disaster Point ID: {disaster_point.id()}")
        distance = calculate_shortest_path(fire_station, disaster_point, road_network_layer)
        response_time = calculate_fastest_time(fire_station, disaster_point, road_network_layer)

# Exit QGIS (for Jupyter, not necessary in QGIS Python console)
qgs.exitQgis()
```

### Explanation:
1. **Layers**: The code loads the fire stations, disaster points, and road network from shapefiles.
2. **Shortest Path Calculation**: It ties the fire stations and disaster points to the road network and uses a graph to compute the shortest path based on road lengths.
3. **Fastest Time Calculation**: It computes the response time by dividing the distance by the average speed (which you can adjust according to your data).
4. **Output**: The code prints the shortest distance in kilometers and the fastest response time in minutes for each pair of fire stations and disaster points.

### Requirements:
- QGIS installation for PyQGIS.
- Shapefiles for road network, fire stations, and disaster points.
- CRS for Freetown should be set to WGS 84 (EPSG:4326).
















To customize the code using different speeds for different road segments, you'll need to modify the road network layer to include speed limits for each road segment. I'll update the code to take speed limits into account when calculating the fastest response time.

### Steps:
1. Ensure your road network shapefile includes a field (e.g., `speed_kmph`) that contains the speed limit for each road segment.
2. The code will calculate travel time for each segment based on the speed limit and accumulate the total time for the path between fire stations and disaster points.

### Updated PyQGIS Code:

```python
import os
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsNetworkAccessManager, QgsPointXY, 
    QgsCoordinateReferenceSystem, QgsDistanceArea, QgsApplication
)
from qgis.analysis import QgsGraphBuilder, QgsGraphAnalyzer
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsFeature, QgsGeometry

# Initialize the QGIS application (for Jupyter, not necessary in QGIS Python console)
QgsApplication.setPrefixPath("/path/to/your/qgis/installation", True)
qgs = QgsApplication([], False)
qgs.initQgis()

# Load the road network, fire stations, and disaster points layers
fire_stations_layer = QgsVectorLayer("path_to_fire_stations.shp", "Fire Stations", "ogr")
disaster_points_layer = QgsVectorLayer("path_to_disaster_points.shp", "Disaster Points", "ogr")
road_network_layer = QgsVectorLayer("path_to_road_network.shp", "Road Network", "ogr")

# Ensure layers are valid
if not fire_stations_layer.isValid() or not disaster_points_layer.isValid() or not road_network_layer.isValid():
    print("One or more layers failed to load")
else:
    print("All layers loaded successfully")

# Set up the coordinate reference system
crs = QgsCoordinateReferenceSystem("EPSG:4326")  # WGS 84 CRS

# Calculate shortest path and fastest time considering speed limits
def calculate_shortest_path_and_time(fire_station, disaster_point, road_network_layer):
    builder = QgsGraphBuilder(crs)
    tied_points = []

    # Get the geometry (fire station and disaster point)
    fire_station_geom = fire_station.geometry().asPoint()
    disaster_geom = disaster_point.geometry().asPoint()

    # Tie the points to the network (find the closest edge)
    tied_fire_station = builder.addVertex(fire_station_geom)
    tied_disaster_point = builder.addVertex(disaster_geom)
    
    tied_points.append(tied_fire_station)
    tied_points.append(tied_disaster_point)

    # Build the graph based on road network, taking speed limits into account
    for feature in road_network_layer.getFeatures():
        geom = feature.geometry()
        
        # Get the length of the road segment in kilometers
        length_km = geom.length() / 1000
        
        # Get the speed limit for this road segment (assuming it's stored in a field 'speed_kmph')
        speed_kmph = feature.attribute('speed_kmph')
        
        if speed_kmph is None or speed_kmph == 0:
            speed_kmph = 50  # Default to 50 km/h if no speed limit is available
        
        # Calculate travel time for this segment (Time = Distance / Speed)
        travel_time_hours = length_km / speed_kmph
        
        # Add the edge with both distance and time as costs
        builder.addEdge(geom.vertexAt(0), geom.vertexAt(1), [length_km, travel_time_hours])

    graph = builder.graph()

    # Compute shortest path (by distance) and fastest path (by time)
    (tree_distance, cost_distance) = QgsGraphAnalyzer.shortestTree(graph, tied_fire_station, 0)
    (tree_time, cost_time) = QgsGraphAnalyzer.shortestTree(graph, tied_fire_station, 1)

    # Output the results
    if cost_distance[tied_disaster_point] == float('inf'):
        print(f"No route found between Fire Station and Disaster Point")
    else:
        distance_km = cost_distance[tied_disaster_point]
        response_time_minutes = cost_time[tied_disaster_point] * 60  # Convert time to minutes
        print(f"Shortest distance: {distance_km:.2f} km")
        print(f"Fastest response time: {response_time_minutes:.2f} minutes")

    return distance_km, response_time_minutes

# Run calculations for all fire stations to disaster points
for fire_station in fire_stations_layer.getFeatures():
    for disaster_point in disaster_points_layer.getFeatures():
        print(f"Calculating for Fire Station ID: {fire_station.id()} and Disaster Point ID: {disaster_point.id()}")
        distance, response_time = calculate_shortest_path_and_time(fire_station, disaster_point, road_network_layer)

# Exit QGIS (for Jupyter, not necessary in QGIS Python console)
qgs.exitQgis()
```

### Key Customizations:
1. **Speed Limit Integration**: 
   - The script assumes that each road segment has a speed limit stored in the attribute `speed_kmph`.
   - If a segment does not have a speed limit, the default speed is set to 50 km/h.
2. **Cost Calculation**: 
   - For each road segment, two costs are calculated: distance (in kilometers) and travel time (in hours). The shortest path is calculated based on distance, and the fastest path is calculated based on travel time.
3. **Output**: 
   - The shortest distance and fastest response time are printed for each pair of fire stations and disaster points.

### Data Requirements:
- The road network shapefile must have a field named `speed_kmph` containing speed limits for each road segment.
- Fire stations and disaster points must be provided as point layers in a valid CRS (preferably WGS 84 for Freetown).

This customized version provides both the shortest distance and the fastest response time based on real-world speed limits. Let me know if you need further adjustments!
