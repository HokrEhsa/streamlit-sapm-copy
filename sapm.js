// Connect to AWS IoT Core
var awsIot = require('aws-iot-device-sdk');

var device = awsIot.device({
   keyPath: './certs/private.pem.key',
  certPath: './certs/certificate.pem.crt',
    caPath: './certs/AmazonRootCA1.pem',
  clientId: 'first-try',
      host: 'a1hmog5cqocf9s-ats.iot.us-east-1.amazonaws.com'
});

// Get current time and store in variable
var current = new Date();

// Subscribe and publish to a topic
device
  .on('connect', function() {
    console.log('connect'); 
    device.subscribe('topic_1');
    device.subscribe('topic_2')

    // Generate random values for each condition
    var air_temperature = getRandomValue(21, 25, 4, 35, -30, 40).toFixed(1);
    var air_humidity = getRandomValue(40, 70, 20, 85, 0, 100).toFixed(0);

    var soil_moisture = getRandomValue(50, 70, 15, 80, 0, 100).toFixed(0);
    var soil_temperature = getRandomValue(12, 25, 4, 30, 0, 40).toFixed(1);
    var soil_ph = getRandomValue(6.0, 7.0, 5.5, 8.0, 1.0, 14.0).toFixed(1);

    var nitrogen_levels = getRandomValue(20, 40, 20, 40, 0, 200).toFixed(0);
    var phosphorus_levels = getRandomValue(10, 20, 10, 20, 0, 150).toFixed(0);
    var potassium_levels = getRandomValue(150, 300, 150, 300, 0, 1999).toFixed(0);

    var motion_detected = Math.round(Math.random());

    // Convert the rounded values back to numbers
    air_temperature = parseFloat(air_temperature);
    air_humidity = parseInt(air_humidity);

    soil_moisture = parseInt(soil_moisture);
    soil_temperature = parseFloat(soil_temperature);
    soil_ph = parseFloat(soil_ph);

    nitrogen_levels = parseInt(nitrogen_levels);
    phosphorus_levels = parseInt(phosphorus_levels);
    potassium_levels = parseInt(potassium_levels);

    // Publish the conditions
    device.publish('topic_1', 
        JSON.stringify({
            time: current.toISOString(),
            device_id: 1,

            air_temperature: air_temperature,
            air_humidity: air_humidity,

            soil_moisture: soil_moisture,
            soil_temperature: soil_temperature,
            soil_ph: soil_ph,

            nitrogen_levels: nitrogen_levels,
            phosphorus_levels: phosphorus_levels,
            potassium_levels: potassium_levels,

            motion_detected: motion_detected
        }));

    
    let hours = current.getHours();
    let minutes = current.getMinutes();
    let seconds = current.getSeconds();
    let day = current.getDate();
    let month = current.getMonth() + 1;
    let year = current.getFullYear();
        
    hours = String(hours).padStart(2, '0');
    minutes = String(minutes).padStart(2, '0');
    seconds = String(seconds).padStart(2, '0');
    day = String(day).padStart(2, '0');
    month = String(month).padStart(2, '0');
    year = String(year);
         
    let formattedTime = `${hours}:${minutes}:${seconds}`;
    let formattedDate = `${day}/${month}/${year}`;

    if(motion_detected==1) {
      var movement_msg = "Movement has been detected by the Passive Infrared (PIR) sensors on your premises. Please refer to the notification titled 'Detection of Pest Infestation' for more information.";
    } else {
      var movement_msg = "No movement has been detected by the Passive Infrared (PIR) sensors on your premises.";
    };

    // Create a table with the environmental conditions
    var table = `
Here are the environmental conditions measured by Device 1 at ${formattedTime} on ${formattedDate}.
———————————
Air Temperature: ${air_temperature}°C
Air Humidity: ${air_humidity}%
Soil Moisture: ${soil_moisture}%
Soil Temperature: ${soil_temperature}°C
Soil pH: ${soil_ph}
Nitrogen Levels: ${nitrogen_levels} mg/kg
Phosphorus Levels: ${phosphorus_levels} mg/kg
Potassium Levels: ${potassium_levels} mg/kg
———————————
${movement_msg}`;

   // Publish the conditions
   device.publish('topic_2', table);
});

// Function to generate a random value for a condition
function getRandomValue(optimalMin, optimalMax, tolerableMin, tolerableMax, min, max) {
    var rand = Math.random();
    if(rand < 0.6) {
        // 60% chance to return a value in the optimal range
        return Math.random() * (optimalMax - optimalMin) + optimalMin;
    } else if(rand < 0.9) {
        // 30% chance to return a value in the tolerable range
        return Math.random() * (tolerableMax - tolerableMin) + tolerableMin;
    } else {
        // 10% chance to return a value in the abnormal range
        return Math.random() * (max - min) + min;
    }
}

// Listen for messages
device
  .on('message', function(topic, payload) {
    console.log('message', topic, payload.toString());
  });