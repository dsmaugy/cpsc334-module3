#include "WiFi.h"
#include <WiFiUdp.h>


#define PHOTO_PIN 35
#define WIFI_SSID "Yale wireless"  # TODO: replace with yale wireless!!
#define WIFI_PASSWORD ""

WiFiUDP Udp;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(PHOTO_PIN, INPUT);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }

  Serial.println(WiFi.localIP());

}

void loop() {
  // put your main code here, to run repeatedly:
  Udp.beginPacket("192.168.0.233", 6100);
  Serial.println(String("begin packet: ") + beginPkt);
  String msg = String(analogRead(PHOTO_PIN));
  Udp.printf(msg.c_str());
  Udp.endPacket();

  Serial.println(String("sent packet: ") + pkt);
  // delay(500);
}
