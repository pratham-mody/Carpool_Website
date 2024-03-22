from flask import Flask, render_template, request, jsonify
from carpool_service import CarpoolService

app = Flask(__name__)
carpool_service = CarpoolService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_ride', methods=['POST'])
def add_ride_route():
    try:
        data = request.get_json()
        pickup = data.get('pickup')
        dropoff = data.get('dropoff')
        if pickup and dropoff:
            carpool_service.add_trip(pickup, dropoff)
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'Missing pickup or dropoff'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/find_carpool', methods=['POST'])
def find_carpool_route():
    data = request.get_json()
    pickup = data.get('pickup')
    dropoff = data.get('dropoff')
    distance = data.get('distance')
    if pickup and dropoff and distance:
        distance_threshold = float(distance)
        best_carpool = carpool_service.find_best_carpool({'pickup': pickup, 'dropoff': dropoff}, distance_threshold)
        print("Best carpool:", best_carpool)
        if best_carpool:
            return jsonify(best_carpool), 200
        else:
            return jsonify({'message': 'No suitable carpool option available.'}), 404
    return jsonify({'error': 'Please provide both pickup and dropoff locations, and maximum distance'}), 400


if __name__ == '__main__':
    app.run(debug=True)
