int leftRight = A0;
int upDown = A1;

int xPosition = 0;
int yPosition = 0;
int SW_state = 0;
int mapX = 0;
int mapY = 0;

int finalXPos = 0;
int finalYPos = 0;

int joystickMidPoint = 512;

void setup() {
  Serial.begin(115200);

}

void loop() {
  delay(1000);
  xPosition = analogRead(upDown);
  yPosition = analogRead(leftRight);
  mapX = map(xPosition, 0, 1023, -512, 512);
  mapY = map(yPosition, 0, 1023, -512, 512);
  
  if (mapX < 0) {
    finalXPos = joystickMidPoint - mapX;
  }

  if (mapX > 0) {
    finalXPos = mapX - joystickMidPoint;
  }

  if (mapY < 0) {
    finalYPos = joystickMidPoint - mapY;
  }

  if (mapY > 0) {
    finalYPos = mapY - joystickMidPoint;
  }

  Serial.println(finalXPos);
  Serial.print(","); // Separator between X and Y
  Serial.print(finalYPos);

}
