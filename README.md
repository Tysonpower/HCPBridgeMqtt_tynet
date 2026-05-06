# Buy a ready to use PCB on [shop.tynet.eu](https://shop.tynet.eu/rs485-bridge-diy-hoermann-mqtt-adapter-esp32-s3-dev-board) :rocket:

If you use a PCB from us, you can get started with our instructions: [Getting started with tynet.eu PCBs](https://github.com/Tysonpower/HCPBridgeMqtt_tynet/wiki)

Would you like to use our ESPHome-based firmware, which offers a few advantages? See our guide: [Getting started with ESPHome](https://github.com/Tysonpower/HCPBridgeMqtt_tynet/wiki/Upgrade-Firmware)

You can find prebuild firmware for our boards in the Firmware folder as non-ESPHome as well as ESPHome version.

# Hörmann HCPBridge for Home Assistant

This repository includes firmware that emulates the Hörmann UAP1-HCP board (Series 4 motors) as well as the older UAP1 that is used for Series 3 motors.
It uses a ESP32 with a RS485 converter and exposes garage door controls over a web page as well as Home Assistant (directly or MQTT).

## Firmware Options

All firmware is optimised for our boards, but it can be used with self build hardware as well with minimal modifications.

### Arduino based Firmware - Series 4 only

Based on a fork of [Gifford47's](https://github.com/Gifford47/HCPBridgeMqtt) and other peoples work it offers a good MQTT based solution with a nice WEB UI and auto discovery for Home Assistant.

This is the default Series 4 firmware for our boards and can also be used with other smart home systems as long as they support MQTT.


### ESPHome based Firmware

Based on a fork of [14yannick's](https://github.com/14yannick/esphome-hcpbridge) and other peoples work it is the best Solution if you use Home Assistant as it directly uses their API and doesen't need MQTT.

Setup is really quick and the Firmware is more stable thanks to ESPome at it's core. Changing the FIrmware or adding Sensors is also simple using the yaml config and recompiling it in ESPHome.
There are two different versions, one for Series 4 and one for Series 3 boards. For this reason we ship our Series 3 boards with the ESPHome based Firmware.
If you don't use Home Assistant you can modify the yaml configuration to use MQTT as well - but you need to compile the firmware yourself to add your credentials.


## Features
- Read door status: open/closed/position, light on/off  
- Control: open, close, stop, light toggle, set position (half/vent/custom)  
- MQTT with Home Assistant Auto Discovery  
- Web Interface for configuration & control  
- OTA Updates  
- First-use hotspot (for out-of-the-box Wi-Fi setup) 
- Optional external sensors (DS18x20, BME280, DHT22, HC-SR04, HC-SR501, MQ4)
- Efficient MQTT traffic (only publish on state change)  
- Support multiple HCP Bridges for multiple garage doors (one bridge per motor)
- Support for ESP32-S3

## Web UI (Arduino based Firmware)

You can use the WebUI for configuration and control of the garage door under.

***http://[deviceip]***

<img width="632" height="790" alt="image" src="https://github.com/user-attachments/assets/a3b047f2-63ca-4785-bbc7-5dc1dd7dba2c" />


<br><br><br><br><br><br><br><br><br><br>

# Build it yourself! 🔨

<details>
 <summary>Step 1: Wiring</summary>

  ## Wiring
 
 ![min wiring](docs/Images/esp32.png)
 
 ESP32 powering requires a Step Down Module such as LM2596S DC-DC, but any 24VDC ==> 5VDC will do, even the tiny ones with 3 pin.
 Please note that the suggested serial pins for serial interfacing, on ESP32, are 16 RXD and 17 TXD.
 
 
 <details>
 <summary>It is possible to implement it with protoboard and underside soldering:</summary>
 
 <br>
 
 ![alt text](docs/Images/esp32_protoboard.jpg)
 ![alt text](docs/Images/esp32_protoboard2.jpg)
 </details>
 
 <details>
 <summary>Details specific to Az-delivery ESP32 (ESP32-WROOM-32)</summary>
 Note the pinout on this cheap but widespread ESP32 module is a bit different. The GND on the bottom left must not be used (it is actually wrongly labeled, it should be CMD). Use the top right instead. Moreover, use the pin 16 as RXD and pin 17 as TXD to match the code on this repository (using UART2, not UART0).
  
 ![image](https://github.com/Gifford47/HCPBridgeMqtt/assets/248961/1ad1c298-cf27-48cc-bf30-7667c27c3304)
 
 </details>
 
 ## RS485
 
 <details open>
 <summary>Pinout RS485 Plug</summary>
 <br>
 
 ![alt text](docs/Images/plug-min.png)
 
 > 📌 **Pinout**
 > 1. GND (Blue)<br>
 > 2. GND (Yellow)<br>
 > 3. B- (Green)<br>
 > 4. A+ (Red)<br>
 > 5. \+24V (Black)<br>
 > 6. \+24V (White)<br>
 
 </details>
 
 ### RS485 adapter
 ![alt text](docs/Images/rs485_raw.jpg)
 > [!NOTE]<br>
 > Pins A+ (Red) and B- (Green) need a 120 Ohm resistor between them for BUS termination. Some RS485 adapters provide termination pad to be soldered.

</details><br>

<details>
 <summary>Step 2: Firmware upload</summary>
 
 ## Upload the firmware
 To use the board without any additional sensors (f.e. as showed in section [wiring](#wiring)) you only need to upload the standard firmware binary.
 
### Sensors
 
 To use additional sensors, you have also to build and upload the according firmware for the sensor. See [flash instructions](docs/flashing_instructions.md) for further info.
 <details>
 <summary>DS18X20 Temperature Sensor</summary>
 
 ![DS18X20](docs/Images/ds18x20.jpg) <br/>
 DS18X20 connected to GPIO4.
 <br>
 
 </details>
 
 <details>
 <summary>HC-SR501 PIR Motion sensor</summary>
 Digital out connected to GPIO23.
 <br>
 </details>
 
 <details>
 <summary>DHT22 temperature and humidity sensor</summary>
 Digital out connected to GPIO27.
 <br>
 </details>
 
 <details>
 <summary>BME280 temperature and humidity sensor</summary>
 
 ![DS18X20](docs/Images/bme280.jpg) <br/>
 SDA connected to  GPIO21<br>
 SCL/SCK connected to GPIO22<br>
 <br>
 </details>
 
 <details>
 <summary>HC-SR04 Ultra sonic proximity sensor</summary>
 
 <br>
 Use the project task for HC-SR04.
 The wiring pins are:<br>
 SR04 Trigger pin is connected to GPIO5<br>
 SR04 ECHO pin is connected to GPIO18<br><br>
 
 It will send an MQTT discovery for two sensor one for the distance in cm available below the sensor and the other informing if the car park is available. It compares if the distance below is less than the maximal measured distance then car park is not available. The hcsr04_maxdistanceCm is defined with 150cm in configuration.h. This setting might not work for everyone. Change it to your needs.
 
 </details>
</details><br>

<details>
  <summary>Step 3: Configuration</summary>

  ## Configuration
  At first boot the settings from the `configuration.h` file are taken over as user preferences. If you choose to make your own build you can set up your settings there.
  After first boot you can change your settings directly in the Web UI without the need to create a new build. 
  
  With the default configuration it will open a Wi-Fi Hotspot you can connect to. When connected to it, you can use the URL http://192.168.4.1 in a web browser to access the Web UI and configure the device.
  
  Use the "Basic Configuration" section to set your Wi-Fi and MQTT credentials, after hitting the Save button your device will reboot.
  The password fields are redacted if there are set with a *. If you don't want to change it, just leave the * as it will be interpreted as unchanged.
  
  <img src="https://github.com/Gifford47/HCPBridgeMqtt/assets/13482963/0081e0bc-ec8e-4cec-a537-c7b0c5758035" width="400" alt="Image of the 'Basic Configuration'">
  
  The preferences will stay even after an OTA update.
  When the memory of your ESP gets deleted your ESP will again load the settings from the configuration.h file.
  
  You can reset all preferences by pressing the BOOT button on the ESP for longer then 5 Seconds and releasing it.
  This will reset all preferences to the default values from configuration.h in the flashed firmware build.
</details><br>

<details>
  <summary>Step 4: Installation and bus scan</summary>
 
  ## Installation
  
  * Connect the board to the BUS
  * Run a BUS scan (differs on the following hardware version): 
  
  ### Old hardware version
  
  BUS scan is started through flipping (ON - OFF) last dip switch. Note that BUS power (+24v) is removed when no devices are detected. In case of issues, you may find useful to "jump start" the device using the +24V provision of other connectors of the motor control board.
    
  ### New hardware version 
  With newer HW versions, the bus scan is carried out using the LC display in menu 37. For more see: [SupraMatic 4 Busscan](https://www.tor7.de/news/bus-scan-beim-supramatic-serie-4-fehlercode-04-vermeiden)
  
  ![alt text](docs/Images/antrieb-min.png)
</details><br>

## Set the ventilation position 

This is just a quick and dirty implementation and needs refactoring, but it is working.
Using the Shutter Custom Card (from HACS) it is also possible to get a representation of the current position of the door, and slide it to custom position (through set_position MQTT command).

The switch for the venting position works with a small hack. Based on the analyses of dupas.me the motor should gave a status 0x0A in venting position. As this was not the case the variable VENT_POS in hciemulator.h was default with value '0x08' which correspond to the position when the garage door is in venting position (position available under ***http://[deviceip]/status***). When the door is stopped in this position the doorstate is set as venting.

<details>
<summary>HomeAssistant shutter cards</summary>

<br>

![Homeassistant card1](docs/Images/ha_shuttercard.png)
![Homeassistant card2](docs/Images/ha.png)
</details>

## Web services

<details>
<summary>Send commands</summary>

URL: **http://[deviceip]/command?action=[id]**
<br>

| id | Function     | Other Parameters |
|----|--------------|------------------|
| 0  | Close        |                  |
| 1  | Open         |                  |
| 2  | Stop         |                  |
| 3  | Ventilation  |                  |
| 4  | Half Open    |                  |
| 5  | Light toggle |                  |
| 6  | Restart      |                  |
| 7  | Set Position | position=[0-100] |

</details>

<details>
<summary>Status report</summary>

URL: **http://[deviceip]/status**
<br>

Response:
```
{
"valid": true,
"doorstate": 64,
"doorposition": 0,
"doortarget": 0,
"lamp": false,
"temp": 19.94000053,
"lastresponse": 0,
"looptime": 1037,
"lastCommandTopic": "hormann/garage_door/command/door",
"lastCommandPayload": "close"
}
```
</details>

<details>
<summary>Wi-Fi status</summary>

URL: **http://[deviceip]/sysinfo**
<br>
</details>

<details>
<summary>OTA Firmware update</summary>

URL: **http://[deviceip]/update**
<br>

![image](https://user-images.githubusercontent.com/14005124/215216505-8c5abe46-5d40-402b-963a-e3825c63d417.png)

</details><br>
