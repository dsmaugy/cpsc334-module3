#include "WiFi.h"
#include "WiFiUdp.h"
#include <ArduinoOSCWiFi.h>

#define WIFI_SSID "The Penthouse"
#define WIFI_PASSWORD ""  // TODO: remove me when push to gitlab
#define CONTROLLER_IP "192.168.0.233"
#define SC_PORT 57120 // default supercollider port
#define PYTHON_PORT 6100
#define LISTEN_PORT 6101

WiFiUDP udp;

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

  udp.begin(LISTEN_PORT);
}

void loop() {
  // OscWiFi.send(CONTROLLER_IP, SC_PORT, "/amen_synth", 0.8, 500);
  // OscWiFi.update();

  int packetSize = udp.parsePacket();
  if (packetSize) {
    char packetBuffer[255];
    int chars = udp.read(packetBuffer, sizeof(packetBuffer));
    Serial.println(packetBuffer);
    if (chars == 1 && packetBuffer[0] == 'R') {
      Serial.println("Record command found");
    }
  }
}
