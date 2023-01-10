#include <Arduino.h>
#include <Sodaq_UBlox_GPS.h>
#include <Wire.h>

#define MySerial        SERIAL_PORT_MONITOR
#define GPSTIME         15UL * 1000
#define LoRaTIME        105UL * 1000
#define BUNDLEDGPS      6

double longitudes[BUNDLEDGPS];
double latitudes[BUNDLEDGPS];
int num_GPS_data;
uint32_t start_LoRa;

void setup() {
    // put your setup code here, to run once:
    delay(3000);
    while (!SerialUSB) {
        // Wait for USB to connect
    }
    
    MySerial.begin(57600);
    sodaq_gps.init(GPS_ENABLE);

    num_GPS_data = 0;
    start_LoRa = millis();
    MySerial.println("Start of code");
    if(sodaq_gps.scan(true,900L * 1000)) {
        MySerial.println(sodaq_gps.getLat());
    }
    else {
        MySerial.println("First fail");
    }
    
}

void loop() {
    // put your main code here, to run repeatedly:
    uint32_t start = millis();
    if (sodaq_gps.scan(true, GPSTIME - 1000)) {
        longitudes[num_GPS_data] = sodaq_gps.getLon();
        latitudes[num_GPS_data] = sodaq_gps.getLat();
        MySerial.println(sodaq_gps.getLat());
    } else {
        longitudes[num_GPS_data] = 0;
        latitudes[num_GPS_data] = 0;
        MySerial.println("fail");
    } 
    
    while (GPSTIME > millis() - start) {
        // Wait for GPS time
    }
    num_GPS_data++;
    if (num_GPS_data >= BUNDLEDGPS) {
        //Send LORA data
        for (size_t i=0;i<BUNDLEDGPS;i++) {
            MySerial.println(String("Point: ") + i);
            MySerial.println(String("Latitude: ") + latitudes[i]);
            MySerial.println(String("Longitude: ") + longitudes[i]);
            
        }
        
        while(LoRaTIME > millis() - start_LoRa) {
          //Wait for LoRa time
        }
        start_LoRa = 0;
    }

}
