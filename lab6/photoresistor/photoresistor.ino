#include "WiFi.h"
#include <WiFiUdp.h>


#define PHOTO_PIN 35
#define WIFI_SSID "streaks"
#define WIFI_PASSWORD "helloyesno"

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
  // Serial.println(analogRead(PHOTO_PIN));
  int beginPkt = Udp.beginPacket("192.168.150.1", 6100);
  Serial.println(String("begin packet: ") + beginPkt);
  uint8_t message[50] = "hello world";
  Udp.write(message, 11);
  int pkt = Udp.endPacket();

  Serial.println(String("sent packet: ") + pkt);
  delay(500);
}
