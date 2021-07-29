# Smart Drink Monitoring System

Repository containing the source code for the User management system and Model personalization engine of the Smart drink monitoring system.

The Smart Drink Monitoring system is a prototype for an interactive IoT Device designed to promote healthier hydration habits in office environments. 

The User management system and the Model personalization engine are conceived as two interfaces through which users can personalize the system and include user-specific data in the model.  

## User management system

The User management system is an application created to customize the preferences of a Human Activity Recognition System. It was designed to work with the Office Hydration Monitoring (OHM) Dataset (https://zenodo.org/record/4681206).

It includes several options to customize the system:

- Name: Defined preferences will be associated with each user name
- Desired level of participation in the proposed interactive scenario:
Three levels of involvement are defined: None, Low, Intermediate or High. This selection determines the number of times the IoT device may ask the user about a specific activity performed.
- Classification mode: This is specific for the OHM Dataset. It allows defining whether the user wants the system to discern between the type of container used: Bottle or Cup/Mug or not.


When cliking "Update preferences" button, those are saved in "preferences.json"
in the format:

{
    "Name": "", 
    "Involvement": "", 
    "Class_type": ""
}


## Model personalization engine

The Model personalization engine is an application created to help users in the process of personalizing Human Activity Recognition models. Its interface allows them to easily and visually provide examples of their own movement patterns.

It was designed to work with M5Stick-C device, capturing motion signals from the accelerometer and the gyroscope sensors. However, it can be addapted to work with other devices. AccX, AccY, AccZ, GyroX, GyroY, GyroZ, Pitch, Roll and Yaw signals are captured, but only AccX, AccY and AccZ signals are be displayed.

Sensing devices are connected via Bluetoothc 4.0 using the Bluepy library. The sensing device need to be trusted by the device running this application and the MAC address of the sensing device need to be included in  "device_mac" variable.

Finally, this device has to be accessible when running this application. Otherwise it will not load the interface.
