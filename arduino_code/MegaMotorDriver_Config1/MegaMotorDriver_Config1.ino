/* 
 *  MegaMotorDriver Control Code
 *  Wilson Ruotolo
 *  2/12/2020
 */

// Setup arrays for motor control pins
int pwmArray[13];
int digArray1[13];
int digArray2[13];

// Function prototypes
void runMotor(int motorSelect, int dir, int pwmVal);

void setup() {
  // Setup all the pwm pins according to current configuration
  pwmArray[1] = 10;   pwmArray[2] = 11;   pwmArray[3] = 9 ;
  pwmArray[4] = 8 ;   pwmArray[5] = 6 ;   pwmArray[6] = 7 ;
  pwmArray[7] = 13;   pwmArray[8] = 12;   pwmArray[9] = 4 ;
  pwmArray[10]= 5 ;   pwmArray[11]= 2 ;   pwmArray[12]= 3 ;

  // Setup all the digital direction setting pins according to current configuration  
  digArray1[1]  = 50;   digArray2[1]  = 48;
  digArray1[2]  = 46;   digArray2[2]  = 44;
  digArray1[3]  = 51;   digArray2[3]  = 49;  
  digArray1[4]  = 47;   digArray2[4]  = 45;  // no forward
  digArray1[5]  = 25;   digArray2[5]  = 27;
  digArray1[6]  = 31;   digArray2[6]  = 29;
  digArray1[7]  = 42;   digArray2[7]  = 40;  
  digArray1[8]  = 38;   digArray2[8]  = 36;
  digArray1[9]  = 22;   digArray2[9]  = 23;  // no backward
  digArray1[10] = 24;   digArray2[10] = 26;  
  digArray1[11] = 28;   digArray2[11] = 30;
  digArray1[12] = 34;   digArray2[12] = 32;  // no backward

  // Start serial comms going at a chosen baud rate
  Serial.begin(115200);
}

void loop() {
  int motorSelect = 0;
  int curDir = 0;
  char incomingByte1 = ' ';
  char incomingByte2 = ' ';
  if (Serial.available() == 2) {
    incomingByte1 = Serial.read();
    incomingByte2 = Serial.read();

    if (incomingByte1 == ' ') {
      stopAll();
    }
    else if (incomingByte1 == '0') {
      motorSelect = 10;
    }
    else if (incomingByte1 == '-') {
      motorSelect = 11;
    }
    else if (incomingByte1 == '=') {
      motorSelect = 12;
    }
    else {
      motorSelect = incomingByte1-'0';
    }
    Serial.print("\nMotor Select: ");
    Serial.print(motorSelect);

    if (incomingByte2 == 'f') {
      curDir = 0;
      Serial.print("    Going forward");
    }
    else if (incomingByte2 == 'b') {
      curDir = 1;
      Serial.print("    Going backward");
    }
    runMotor(motorSelect, curDir, 150);
    while(Serial.available() > 0) {
      Serial.read();
    }
  }
//  else{
//    while(Serial.available() > 0) {
//      Serial.read();
//    }
//  }
}

void runMotor(int motorSelect, int dir, int pwmVal) {
  analogWrite(pwmArray[motorSelect], pwmVal);
  if (dir == 0) {
    digitalWrite(digArray1[motorSelect], HIGH);
    digitalWrite(digArray2[motorSelect], LOW);
  }
  else if (dir == 1) {
    digitalWrite(digArray1[motorSelect], LOW);
    digitalWrite(digArray2[motorSelect], HIGH);
  }
}

void stopAll() {
  for (int i = 1; i<=12; i++) {
    runMotor(i,0,0); 
  }
  Serial.println("\nStopping All Motors");
}
