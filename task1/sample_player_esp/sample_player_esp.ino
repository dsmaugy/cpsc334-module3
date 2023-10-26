// #include <WiFiUdp.h>
// #include <OSCMessage.h>
#include "WiFi.h"
#include <ArduinoOSCWiFi.h>

#define WIFI_SSID "streaks"
#define WIFI_PASSWORD "helloyesno"
// #define SC_IP "172.29.129.145"
#define SC_IP "192.168.150.51"
#define SC_PORT 57120 // default supercollider port

// WiFiUDP Udp;

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
  // OSCMessage msg("/amen_synth");
  // msg.add(0.8);
  // msg.add(500);
  // Udp.beginPacket(SC_IP, SC_PORT);
  // msg.send(Udp);
  // Udp.endPacket();
  // msg.empty();

  OscWiFi.send(SC_IP, SC_PORT, "/amen_synth", 0.8, 500);
  OscWiFi.update();
  // Serial.println("Sent OSC msg");
}
