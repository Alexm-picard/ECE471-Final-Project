// Function to update hollow semi-circle gauges
function updateGauge(elementId, value, maxValue) {
    const progressElement = document.getElementById(`${elementId}-progress`);
    const valueElement = document.getElementById(`${elementId}-value`);

    // Calculate percentage and rotation angle
    const percentage = Math.min((value / maxValue) * 100, 100);
    const angle = (percentage / 100)*180; // Semi-circle: 0 to 180 degrees
    // Update gauge rotation
    progressElement.style.transform = `rotate(${angle-45}deg)`; // Rotate from -90 to +90 degrees

    // Update the value displayed inside the gauge
    valueElement.innerText = `${value.toFixed(1)}`;
}

// Function to fetch and update sensor data
async function updateData() {
    try {
        const response = await fetch('/api/sensor_data');
        if (!response.ok) throw new Error('Failed to fetch data');

        const data = await response.json();

        // Update MiCS 5524 (Voltage)
        updateGauge('voltage', data.MiCS_5524, 5); // Assume 5V max

        // Update SGP30 (eCO2)
        updateGauge('eco2', data.SGP30_co2, 2000); // Assume 2000 ppm max

        // Update SGP30 (TVOC)
        updateGauge('tvoc', data.SGP30_tvoc, 1000); // Assume 1000 ppb max
	
    } catch (error) {
        console.error('Error updating data:', error);
    }
}

// Update every second
setInterval(updateData, 1000);
updateData();
