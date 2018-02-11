# Raspberry Pi Sensor Controller
### Raspberry Pi Code

#### Description
Fourth year college project to allow an Android app to control the sensors on a Rapberry Pi with GrovePi over AWS IoT Core. This is the Raspberry Pi codebase.   
This project is a work in progress...

#### Sensor Configuration
The application runs two threads: a publisher and subscriber.
The subscriber listens to the MQTT channel "sensor_config" and is expecting data in the following JSON format:
```
{
  "message":
  {
    "port_id":"D7",
    "sensor_type":"button",
    "display_name":"Button",
    "sample_rate":1,
    "is_enabled":true
  }
}
```

Each sensor has a **sensor_type** string value that tells the Pi what code to run to read that sensor's date.
Sensor Types will be formatted like this: **I am a sensor type**  
The following sensors are supported:
- Button - **button**
- Ultrasonic Rangefinder - **rangefinder**
- Sound Sensor - **sound**
- Temperature and Humidity Sensor - **temperature_humidity**
- Light Sensor - **light**
- Potentiometer / Rotary Angle Sensor - **potentiometer**

The index for the sensor array is the port_id. If a message is sent on a specific port, then the sensor configuration on that port will be overwritten.
For example:
- Configure BUTTON on PORT D7
- Configure RANGEFINDER on PORT D7

The RANGEFINDER will overwrite the BUTTON.  
To stop reading a port while keeping the sensor configuration, send the same configuration again with "is_enabled" set to false.

#### Readings
When a sensor reads and publishes its data, it will be sent in the following JSON format over the "readings" MQTT channel:
```
{
  "sensor_type": "rangefinder",
  "reading": "3",
  "port_id": "D5"
}
```
The only exception is the Temperature and Humidity sensor, which sends it in the following way:
```
{
  "sensor_type": "temperature_humidity",
  "reading": "{\"temperature\": \"20.0\", \"humidity\": \"23.0\"}",
  "port_id": "D6"
}
```

#### Instructions
This repository codebase is designed to be ran on a Raspberry Pi with a GrovePi component installed.

The standard project structure is as follows:
* college-iot_pi_controller_thing/
  * README.MD
  * start.sh
  * bin/
    * .py files
  * config/
    * aws.config.template
    * sensors.config.template
    * aws.config
    * sensors.config
    * certs/
      * root_ca.key
      * certificate.pem.crt
      * private.pem.key
      * public.pem.key

##### Step 1: Configure AWS
Create an IoT Thing on your AWS IoT Core console and make note of the following information:
- Thing Name     (To be used as the Client ID)
- Endpoint       (Found under IoT Core settings)

Download the following certificates from your Thing's credentials page:
- Root CA
- Certificate
- Private Key

Copy the downloaded certificates to...   
`college-iot_pi_controller_thing/config/certs/root_ca.key`   
`college-iot_pi_controller_thing/config/certs/certificate.pem.crt`   
`college-iot_pi_controller_thing/config/certs/private.pem.key`

Copy the file   
`college-iot_pi_controller_thing/config/aws.config.template`   
to   
`college-iot_pi_controller_thing/config/aws.config`.

Under the new aws.config file you created, fill in the XML values with the information you noted previously.

##### Step 2: Start the Pi application
Navigate to the `start.sh` file under the project root.  
Ensure the file is executable by typing `sudo chmod +x start.sh`  
The application can then be started by typing `./start.sh`  
This bash script will check that you're running the script on a Raspberry Pi and if Python is installed.  
Once the checks pass, the Python code will be called and the application will start.

#### Step 3: Start the Android App
WIP