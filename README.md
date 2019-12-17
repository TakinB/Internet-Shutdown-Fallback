
* This program is written for ESP8266
 *  Make sure all the html, font, and all fron end is in a folder called data
 *  Make sure this sketch is in the same root as data
 *  First upload this Arduino code to the ESP8266
 *  Then in Arduino IDE navigate to tools>ESP8266 Sketch Data Upload  
 *  upload the data folder to ESP8266
 *  Make sure in the tools tab, you have the right flash size selected (4Mb) and size of OTA is more than the data folder size
 *  For example I've chosen 4Mb and 1019Kb as the OTA in the tools>flash size
 *  
 *  
 *  This code creates a WiFi access point 
 *  provides a web server on it which pops up automatically upon sign in to the Wi-Fi 
