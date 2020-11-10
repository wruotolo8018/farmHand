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
void stopAll();

void setup() {
  
  // Setup all the digital direction setting pins according to current configuration  
  for (int i = 0; i<54; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }

    // Finger 1
  pwmArray[1] = 8;   pwmArray[2] = 9;   
  digArray1[1]  = 46;   digArray2[1]  = 48;
  digArray1[2]  = 50;   digArray2[2]  = 52;

  // Finger 2
  pwmArray[3] = 2;   pwmArray[4] = 3;   
  digArray1[3]  = 47;   digArray2[3]  = 49;
  digArray1[4]  = 51;   digArray2[4]  = 53;

  // Finger 3
  pwmArray[5] = 4;   pwmArray[6] = 5;   
  digArray1[5]  = 41;   digArray2[5]  = 43;
  digArray1[6]  = 37;   digArray2[6]  = 39;

  // Finger 4
  pwmArray[7] = 6;   pwmArray[8] = 7;   
  digArray1[7]  = 27;   digArray2[7]  = 29;
  digArray1[8]  = 31;   digArray2[8]  = 33;

  // Start serial comms going at a chosen baud rate
  Serial.begin(115200);
}

char inChar;
int readLength = 0; 
int num_motors = 8;
int pwm1 = 0;
int mappedPWM = 0;
int curTime = millis();
int prevTime = millis();
int printInterval = 3000;
int pwmValArray[13];
int pwmDirArray[13]; // just for debugging

bool printing = false;

void loop() {
  curTime = millis();

  if (Serial.available() > 0){
    readLength = Serial.available();

    if (readLength == 18) {
      // Read inputs and process
      String inString = "";
      while(Serial.available() > 0) {
        inChar = Serial.read();
        inString += inChar;
      }
//      Serial.print(inString);
      
      // Map inString to separate motor commands and save in array
      for (int i = 0; i<9; i++) {
        char firstDigit = inString[i*2];
        char secondDigit = inString[i*2+1];
        int firstDigitInt = firstDigit - '0';
        int secondDigitInt = secondDigit - '0';
        int pwmValTemp = firstDigitInt*10 + secondDigitInt;
        pwmValArray[i+1] = pwmValTemp;
      }

      // Iterate through motors and set direction and pwm from associated arrays
      for (int i = 1; i<=num_motors; i++) {
        int hundoPWM = pwmValArray[i];
        if (hundoPWM > 50) { 
          mappedPWM = map(hundoPWM, 50, 99, 0, 255);
          runMotor(i,0,mappedPWM);
          pwmDirArray[i] = 0;
        }
        else if (hundoPWM < 50) { 
          mappedPWM = map(hundoPWM, 50, 0, 0, 255);
          runMotor(i,1,mappedPWM);
          pwmDirArray[i] = 1;
        }
        else {
          runMotor(i,0,0);
        }
      }

//      Serial.print("\nMotor values: ");
//      for (int i = 1; i <= 9; i++) {
//        Serial.print(pwmValArray[i]);
//        Serial.print(":");
//        Serial.print(pwmDirArray[i]);
//        Serial.print("  ");
//      }
//      Serial.print("\n");
      
      while (Serial.available() > 0) {
          Serial.read();  
      }
    }
    else if (readLength > 18) {
      while (Serial.available() > 0) {
        Serial.read();  
      }
    }
  }
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
