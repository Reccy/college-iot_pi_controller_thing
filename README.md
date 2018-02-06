# Raspberry Pi Sensor Controller
### Raspberry Pi Code

#### Description
Fourth year college project to allow an Android app to control the sensors on a Rapberry Pi with GrovePi over AWS IoT Core. This is the Raspberry Pi component.   
This project is a work in progress...

#### Instructions
This repository codebase is designed to be ran on a Raspberry Pi with a GrovePi component installed.

The standard project structure is as follows:
* college-iot_pi_controller_thing/
  * config/
    * aws.config.template
    * sensors.config.template
    * aws.config
    * sensors.config
    * certs/
      * root_ca.key
      * certificate.pem.crt
      * private.pem.key

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

##### Step 2: ???
Work in Progress
