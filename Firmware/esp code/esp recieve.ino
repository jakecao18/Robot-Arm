#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>
#include <WiFi.h>

#define STEP_PIN 2
#define DIR_PIN 4
#define EN_PIN 23

long currentSteps = 0;
long targetSteps = 0;
long elbowCurrent = 90;
long wristPitchCurrent = 90;
long shoulderCurrent = 90;

unsigned long lastStepTime = 0;
const unsigned long stepInterval = 7000;  // microseconds

const char* ssid = "westlake2022";
const char* password = "workIsFUN2023";

WiFiUDP udp;

const int UDP_PORT = 5000;

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

//array of max and min of servos 0 - 4
//calibrated servos 0, 1, & 2 
int servoMax[] = {2930, 3000, 3000, 2750, 2750};
int servoMin[] = {480, 450, 450, 500, 500};

//function that converts angle into pwm pulse
void writeAngle(int servoNum, double angle){
  //servo-0 has a range of 270 degrees therefor needing seperate mapping
  if(servoNum == 0){
    angle = constrain(angle, 0, 270);
    double pwmSignal = map(angle, 0, 270, servoMin[servoNum], servoMax[servoNum]);
    pwm.writeMicroseconds(servoNum, pwmSignal);
  }
  else if(servoNum == 1 || servoNum == 2){
    angle = constrain(angle, 0, 298);
    double pwmSignal = map(angle, 0, 298, servoMin[servoNum], servoMax[servoNum]);
    pwm.writeMicroseconds(servoNum, pwmSignal);
  }
  else{
    angle = constrain(angle, 0, 270);
    double pwmSignal = map(angle, 0, 270, servoMin[servoNum], servoMax[servoNum]);
    pwm.writeMicroseconds(servoNum, pwmSignal);
    Serial.print(pwmSignal);
  }
}

void setStepperAngle(float angle) {
  // Convert angle to absolute step position
  targetSteps = round(angle / 1.8);
}

void runStepper() {
  // Already at target
  if (currentSteps == targetSteps) {
    return;
  }
  // Don't step too quickly
  if (micros() - lastStepTime < stepInterval) {
    return;
  }

  lastStepTime = micros();

  // Need to move forward
  if (targetSteps > currentSteps) {
    digitalWrite(DIR_PIN, HIGH);

    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(2);
    digitalWrite(STEP_PIN, LOW);

    currentSteps++;
  }

  // Need to move backward
  else {
    digitalWrite(DIR_PIN, LOW);

    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(2);
    digitalWrite(STEP_PIN, LOW);

    currentSteps--;
  }
}

void setup() {
  //initialize pwm
  pwm.begin();
  pwm.setPWMFreq(50);

  pinMode(23, OUTPUT);
  digitalWrite(23, LOW);

  WiFi.begin(ssid, password);
  Serial.begin(115200);

  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected!");

  Serial.print("ESP32 IP address: ");
  Serial.println(WiFi.localIP());

  udp.begin(UDP_PORT);

  Serial.print("Listening on UDP port: ");
  Serial.println(UDP_PORT);

  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(EN_PIN, OUTPUT);

  // Enable A4988
  digitalWrite(EN_PIN, LOW);
  digitalWrite(DIR_PIN, HIGH);

}

void moveShoulderSlow(int targetShoulder) {

  while (shoulderCurrent != targetShoulder) {

    if (shoulderCurrent < targetShoulder)
      shoulderCurrent++;
    else if (shoulderCurrent > targetShoulder)
      shoulderCurrent--;

    writeAngle(0, shoulderCurrent);

    delay(15);
  }
}


void moveElbowSlow(int targetElbow) {

  while (elbowCurrent != targetElbow) {

    if (elbowCurrent < targetElbow)
      elbowCurrent++;
    else if (elbowCurrent > targetElbow)
      elbowCurrent--;

    writeAngle(1, elbowCurrent);

    delay(15);
  }
}


void moveWristPitchSlow(int targetWristPitch) {

  while (wristPitchCurrent != targetWristPitch) {

    if (wristPitchCurrent < targetWristPitch)
      wristPitchCurrent++;
    else if (wristPitchCurrent > targetWristPitch)
      wristPitchCurrent--;

    writeAngle(2, wristPitchCurrent);

    delay(15);
  }
}

void loop() {

  int packetSize = udp.parsePacket();

  if (packetSize > 0) {

    char packet[256];

    int length = udp.read(packet, 255);
    packet[length] = '\0';

    Serial.print("Received: ");
    Serial.println(packet);

    JsonDocument data;

    DeserializationError error = deserializeJson(data, packet);

    if (error) {
      Serial.println("JSON error");
      return;
    }

    float base = data["base"];
    float shoulder = data["shoulder"];
    float elbow = data["elbow"];
    float wristPitch = data["wristPitch"];
    float wristRoll = data["wristRoll"];
    float gripper = data["gripper"];
    float esp_check = data["esp_check"];

    if (base == 0 && shoulder == 67.5 && elbow == 0 && wristPitch == 270 && esp_check == 1){
      moveShoulderSlow(shoulder);
      delay(1000);
      moveWristPitchSlow(wristPitch);
      delay(1000);
      moveElbowSlow(elbow);
      delay(1000);
      setStepperAngle(base);
      while(currentSteps != targetSteps){
        runStepper();
      }
      delay(1000);
    } else if (shoulder != 67.5 && esp_check == 1) {
      setStepperAngle(base);
      while(currentSteps != targetSteps){
        runStepper();
      }
      delay(1000);
      moveElbowSlow(elbow);
      moveWristPitchSlow(wristPitch);
      moveShoulderSlow(shoulder);
    }
    else if (esp_check == 0) {
      setStepperAngle(base);
      while(currentSteps != targetSteps){
        runStepper();
      }
      writeAngle(4, gripper);
      moveElbowSlow(elbow);
      moveWristPitchSlow(wristPitch);
      writeAngle(3, wristRoll);
      moveShoulderSlow(shoulder);
    }
  }
}

