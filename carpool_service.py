import requests
import csv
import math

import os

class CarpoolService:
    def __init__(self):
        self.geocoding_api_key = 'AIzaSyCiK_BbIXq8mIXdqaAPxf4WG9LwM2_CYkk'
        self.distance_matrix_api_key = 'AIzaSyD3ltf6E3Amq_jB1g4Hn1asaQfSwvAlcSY'
        self.trip_data_file = os.path.join(os.path.dirname(__file__), 'static', 'trip_data.csv')

    def geocode_address(self, address):
        print("Geocoding address:", address)  # Add this line
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={self.geocoding_api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                print("Geocoding API returned status:", data['status'])
        else:
            print("Error calling Geocoding API. Status code:", response.status_code)
            print("Response content:", response.content)
        return None, None

    def calculate_distance(self, origin_coords, destination_coords):
        print("Calculating distance between:", origin_coords, destination_coords)  # Add this line
        if origin_coords and destination_coords:
            url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={origin_coords[0]},{origin_coords[1]}&destinations={destination_coords}&key={self.distance_matrix_api_key}'
            response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                element = data['rows'][0]['elements'][0]
                if 'distance' in element:
                    distance = element['distance']['value'] / 1000  # Distance in kilometers
                    return distance
                else:
                    print("Distance information not available. Using fallback mechanism.")
                    return self.calculate_straight_line_distance(origin_coords, destination_coords)
            else:
                print("Distance Matrix API returned status:", data['status'])
        else:
            print("Error calling Distance Matrix API. Status code:", response.status_code)
            print("Response content:", response.content)
        return None


    def calculate_straight_line_distance(self, origin_coords, destination_coords):
        lat1, lon1 = origin_coords
        lat2, lon2 = destination_coords
        # Radius of the Earth in kilometers
        radius = 6371.0
        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        # Calculate differences in latitude and longitude
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        # Calculate the distance using the haversine formula
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = radius * c
        return distance

    def read_trip_data(self):
        trip_data = []
        with open(self.trip_data_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                trip_data.append(row)
        return trip_data

    def write_trip_data(self, trip_data):
        with open(self.trip_data_file, 'w', newline='') as file:
            fieldnames = ['pickup', 'dropoff']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for trip in trip_data:
                writer.writerow(trip)

    def add_trip(self, pickup_address, dropoff_address):
        trip_data = self.read_trip_data()
        trip_data.append({'pickup': pickup_address, 'dropoff': dropoff_address})
        self.write_trip_data(trip_data)

    def find_best_carpool(self, new_request, distance_threshold):
        new_pickup = new_request['pickup']
        new_dropoff = new_request['dropoff']

        best_carpool = None
        existing_requests = self.read_trip_data()

        for req in existing_requests:
            pickup_address = req['pickup']
            dropoff_address = req['dropoff']
            pickup_coords = self.geocode_address(pickup_address)
            dropoff_coords = self.geocode_address(dropoff_address)
            new_pickup_coords = self.geocode_address(new_pickup)
            distance1 = self.calculate_distance(new_pickup_coords, pickup_coords)
            distance2 = self.calculate_distance(dropoff_coords, new_dropoff)
            print("Distances:", distance1, distance2)
            if distance1 is not None and distance2 is not None and distance1 + distance2 <= distance_threshold:
                best_carpool = req
                break

        return best_carpool

# Example usage
if __name__ == "__main__":
    carpool_service = CarpoolService()

    while True:
        print("1. Add a trip")
        print("2. Find a ride along")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            pickup_address = input("Enter pickup address: ")
            dropoff_address = input("Enter dropoff address: ")
            carpool_service.add_trip(pickup_address, dropoff_address)
        elif choice == '2':
            pickup_address = input("Enter pickup address: ")
            dropoff_address = input("Enter dropoff address: ")
            distance_threshold = float(input("Enter the maximum distance threshold (in kilometers): "))
            best_carpool = carpool_service.find_best_carpool({'pickup': pickup_address, 'dropoff': dropoff_address}, distance_threshold)
            if best_carpool:
                print("Best carpool option available.")
                print("Pickup: ", best_carpool['pickup'])
                print("Dropoff: ", best_carpool['dropoff'])
            else:
                print("No suitable carpool option available.")
        else:
            print("Invalid choice. Please enter 1 or 2.")