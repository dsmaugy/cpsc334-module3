#include "WiFi.h"
#include <ArduinoOSCWiFi.h>

#define WIFI_SSID "The Penthouse"
#define WIFI_PASSWORD ""
#define SC_IP "192.168.0.233"
#define SC_PORT 57120 // default supercollider port


void setup() {
  Serial.begin(9600);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println();
  Serial.println(WiFi.localIP());

}

void loop() {
  OscWiFi.send(SC_IP, SC_PORT, "/amen_synth", 0.8, 500);
  OscWiFi.update();
  // Serial.println("Sent OSC msg");
}
