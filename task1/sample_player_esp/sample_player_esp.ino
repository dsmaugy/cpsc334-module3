#include "WiFi.h"
#include "WiFiUdp.h"
#include <ArduinoOSCWiFi.h>

// networking constants
#define WIFI_SSID "The Penthouse"
#define WIFI_PASSWORD ""  // TODO: remove me when push to gitlab
#define CONTROLLER_IP "192.168.0.233"
#define SC_PORT 57120 // default supercollider port
#define PYTHON_PORT 6100
#define LISTEN_PORT 6101

// hardware pins
#define PIEZO 1
#define D_TILT_FORWARD 1
#define D_TILT_RIGHT 1
#define STATUS_LED 1

// machine states
#define STATUS_IDLE = 0
#define STATUS_RECORDING = 1

// timings
#define LED_BLINK_THRESH = 100
#define RECORDING_LENGTH = 1000*10

WiFiUDP udp;
int currentStatus;
unsigned long lastBlinkTime;
unsigned long recordingStart;

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

  currentStatus = STATUS_IDLE:
  lastBlinkTime = millis();

  // single state change messages should really be done with TCP for relability
  udp.begin(LISTEN_PORT);
}

void loop() {
  // OscWiFi.send(CONTROLLER_IP, SC_PORT, "/amen_synth", 0.8, 500);
  // OscWiFi.update();

  if (currentStatus == STATUS_IDLE) {
    digitalWrite(STATUS_LED, HIGH);

    int packetSize = udp.parsePacket();
    if (packetSize) {
      char packetBuffer[255];
      int chars = udp.read(packetBuffer, sizeof(packetBuffer));
      Serial.println(packetBuffer);
      if (chars == 1 && packetBuffer[0] == 'R') {
        Serial.println("Record command found");
        recordingStart = millis();
        currentStatus = STATUS_RECORDING;
      }
    }
  } else if (currentStatus == STATUS_RECORDING) {
    if (millis() - lastBlinkTime >= LED_BLINK_THRESH) {
      digitalWrite(STATUS_LED, !digitalRead(STATUS_LED));
      lastBlinkTime = millis();
    }
    
    send_to_sc();
  }
}

void send_to_sc() {

  if (millis() - recordingStart >= RECORDING_LENGTH) {
    // switch back to IDLE mode and tell the controller that the audio has finished
  } else {
    // send sensor data to supercollider
  }
}
