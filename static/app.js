document.addEventListener('DOMContentLoaded', function() {
    // Function to handle adding a ride
    function addRide() {
        // Get pickup and dropoff addresses from input fields
        var pickup = document.getElementById('pickupAddress').value;
        var dropoff = document.getElementById('dropoffAddress').value;
        
        // Make a POST request to the server to add the ride
        fetch('/add_ride', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pickup: pickup,
                dropoff: dropoff
            })
        })
        .then(response => response.json())
        .then(data => {
            // Display success or error message
            if (data.success) {
                alert('Ride added successfully!');
            } else {
                alert('Error adding ride. Please try again.');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while processing your request. Please try again.');
        });
    }

    // Function to handle finding a carpool
    function findCarpool() {
        // Get pickup, dropoff, and distance values from input fields
        var pickup = document.getElementById('pickupAddressCarpool').value;
        var dropoff = document.getElementById('dropoffAddressCarpool').value;
        var distance = document.getElementById('distanceCarpool').value;
        
        // Make a POST request to the server to find a carpool
        fetch('/find_carpool', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pickup: pickup,
                dropoff: dropoff,
                distance: distance
            })
        })
        .then(response => response.json())
        .then(data => {
            // Display carpool result
            if (data.pickup && data.dropoff) {
                alert('Best carpool option available.\nPickup: ' + data.pickup + '\nDropoff: ' + data.dropoff);
            } else {
                alert('No suitable carpool option available.');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while processing your request. Please try again.');
        });
    }
    

    // Attach event listeners to buttons
    document.getElementById('addRideButton').addEventListener('click', addRide);
    document.getElementById('findCarpoolButton').addEventListener('click', findCarpool);
});
