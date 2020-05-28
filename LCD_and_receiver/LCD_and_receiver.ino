// Feather9x_RX
// -*- mode: C++ -*-
// Example sketch showing how to create a simple messaging client (receiver)
// with the RH_RF95 class. RH_RF95 class does not provide for addressing or
// reliability, so you should only use RH_RF95 if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example Feather9x_TX

#include <SPI.h>
#include <RH_RF95.h>
#include <Regexp.h>
//#include <LiquidCrystal.h>


#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library for ST7735
#include <SPI.h>

// For Ywrobot LCD screen
#define TFT_CS         12
#define TFT_RST        5
#define TFT_DC         13

// For 1.8" TFT with ST7735 use:
Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

// for Feather32u4 RFM9x
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 7

float p = 3.1415926;

/* for feather m0 RFM9x
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3
*/

/* for shield 
#define RFM95_CS 10
#define RFM95_RST 9
#define RFM95_INT 7
*/

/* Feather 32u4 w/wing
#define RFM95_RST     11   // "A"
#define RFM95_CS      10   // "B"
#define RFM95_INT     2    // "SDA" (only SDA/SCL/RX/TX have IRQ!)
*/

/* Feather m0 w/wing 
#define RFM95_RST     11   // "A"
#define RFM95_CS      10   // "B"
#define RFM95_INT     6    // "D"
*/
/*
#if defined(ESP8266)
  // for ESP w/featherwing
  #define RFM95_CS  2    // "E"
  #define RFM95_RST 16   // "D"
  #define RFM95_INT 15   // "B"

#elif defined(ESP32)  
  // ESP32 feather w/wing 
  #define RFM95_RST     27   // "A"
  #define RFM95_CS      33   // "B"
  #define RFM95_INT     12   //  next to A

#elif defined(NRF52)  
  // nRF52832 feather w/wing
  #define RFM95_RST     7   // "A"
  #define RFM95_CS      11   // "B"
  #define RFM95_INT     31   // "C"
  
#elif defined(TEENSYDUINO)
  // Teensy 3.x w/wing
  #define RFM95_RST     9   // "A"
  #define RFM95_CS      10   // "B"
  #define RFM95_INT     4    // "C"
#endif
*/

// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 915.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

//LiquidCrystal lcd(10, 9, 6, 5, 3, 2);

char strReceived[140];
MatchState ms;
String receivedParagraph = "";

uint16_t color = 0xF800;

  
void setup()
{
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  
  Serial.begin(9600);
  
  //while (!Serial) {
  //  delay(1);
  //}
  delay(10);
    
  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    Serial.println("Uncomment '#define SERIAL_DEBUG' in RH_RF95.cpp for detailed debug info");
    //lcd.home();
    //lcd.print("LoRa radio init failed");
      Serial.println("LoRa radio init failed");
      //printLCD("LoRa radio init failed", ST77XX_MAGENTA, 0);
    while (1);
  }
  Serial.println("LoRa radio init OK!");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    //lcd.home();
    //lcd.print("setFrequency failed");
    Serial.println("setFrequency failed");
    //printLCD("setFrequency failed", ST77XX_MAGENTA, 0);
    while (1);
  }
  Serial.print("Set Freq to: "); 
  Serial.println(RF95_FREQ);
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);

  // Use this initializer if using a 1.8" TFT screen:
  tft.initR(INITR_BLACKTAB);      // Init ST7735S chip, black tab
  //screen warmup
  tft.fillScreen(ST77XX_BLACK);
  newsTemplate(ST77XX_GREEN);

  //tft.fillScreen(ST77XX_BLACK);
}

void loop()
{
     //Serial.println("Welcome to our demo ****!");
    //printLCD("Welcome to our demo!", ST77XX_MAGENTA, 0);
  if (rf95.available())
  {
    // Should be a message for us now
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);


    if (rf95.recv(buf, &len))
    {
      //RH_RF95::printBuffer("Received: ", buf, len);
      
      memcpy(strReceived,((char*)buf),len);
      
      //Serial.print("Got: ");
      //Serial.println((char*)buf);     
      Serial.println(strReceived);
      
      Serial.print("RSSI: ");
      Serial.print(rf95.lastRssi(), DEC);
      Serial.println("dBm");

      //Serial.println();
       ms.Target (strReceived);
       char result = ms.Match ("PROTOCOLE", 0);
       char refreshPressed = ms.Match ("REFRESH", 0);
       
       if (result != REGEXP_MATCHED && refreshPressed != REGEXP_MATCHED)
       {
         // matching offsets in ms.capture
          receivedParagraph = receivedParagraph + strReceived;
          Serial.println("MATCHED PROTOCOL");
          Serial.println(receivedParagraph);
          //Serial.println(Tostms);
          Serial.println("result:");
          Serial.println(result);
          Serial.println("refresh:");
          Serial.println(refreshPressed);
       }else if (refreshPressed == REGEXP_MATCHED)
       {
          Serial.println("MATCHED REFRESH");
          tft.fillScreen(ST77XX_BLACK);
          newsTemplate(ST77XX_GREEN);
       } 
       else {
          receivedParagraph = "";
         // tft.fillScreen(ST77XX_BLACK);
       }
       
        //lcd.clear();
        delay(300);
        //lcd.print(receivedParagraph);
        Serial.println(receivedParagraph);
        printLCD(receivedParagraph, ST77XX_WHITE, 1);
        //delay(1000);
        //tft.fillScreen(ST77XX_BLACK);
        //newsTemplate(ST77XX_GREEN);
    }
    else
    {
      Serial.println("Receive failed");
    }


  }
    // set the cursor to column 0, line 1
    // (note: line 1 is the second row, since counting begins with 0):
    //lcd.setCursor(0, 0);
    // print the number of seconds since reset:
    //lcd.print(millis() / 1000);


}

void printLCD(String text, uint16_t myColor, int fontSize)
{
  //tft.fillScreen(ST77XX_BLACK);
  tft.setCursor(0, 30);
  tft.setTextWrap(true);
  tft.setTextColor(myColor); //ST77XX_WHITE ST77XX_RED  ST77XX_YELLOW  ST77XX_GREEN ST77XX_BLUE
  tft.setTextSize(fontSize); // 0 1 2 3 4 5 6 ...
  tft.println(text);
}

void newsTemplate(uint16_t color) {
  tft.fillScreen(ST77XX_BLACK);
  tft.setCursor(5, 5);
  tft.setTextColor(ST77XX_GREEN); //ST77XX_WHITE ST77XX_RED  ST77XX_YELLOW  ST77XX_GREEN ST77XX_BLUE
  tft.setTextSize(2); // 0 1 2 3 4 5 6 ...
  tft.println("HEADLINE");
  tft.drawFastHLine(0, 25, tft.width(), color);

}
