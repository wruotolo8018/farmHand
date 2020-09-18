/* 
 *  MegaMotorDriver Control Code
 *  Wilson Ruotolo
 *  9/17/2020
 */

// Setup arrays for motor control pins
int pwmArray[7];
int digArray1[7];
int digArray2[7];

// Function prototypes
void runMotor(int motorSelect, int dir, int pwmVal);
void stopAll();

void setup() {
  // Setup all the pwm pins according to current configuration

  // Finger 1
  pwmArray[1] = 11;   pwmArray[2] = 10;   
  
  
//  pwmArray[3] = 9 ;
//  pwmArray[7] = 13;   pwmArray[8] = 12;   pwmArray[9]= 2 ;
//
//  pwmArray[4] = 8 ;   pwmArray[5]  = 6 ;   pwmArray[6] = 7 ;
//  pwmArray[10]= 5 ;   pwmArray[11] = 4 ;   pwmArray[12]= 3 ;

  // Setup all the digital direction setting pins according to current configuration  
  for (int i = 22; i<53; i++) {
    pinMode(i, OUTPUT);
  }
  
  // Finger 1
  digArray1[1]  = 0;   digArray2[1]  = 1;
  digArray1[2]  = 2;   digArray2[2]  = 3;

  
//  digArray1[3]  = 51;   digArray2[3]  = 49;  
//  
//  // Thumb
//  digArray1[7]  = 42;   digArray2[7]  = 40;  
//  digArray1[8]  = 38;   digArray2[8]  = 36;
//  digArray1[9]  = 28;   digArray2[9]  = 30;
//  
//  // Finger 2
//  digArray1[4]  = 47;   digArray2[4]  = 45;
//  digArray1[5]  = 25;   digArray2[5]  = 27;
//  digArray1[6]  = 31;   digArray2[6]  = 29; 

  // Start serial comms going at a chosen baud rate
  Serial.begin(115200);
}

char inChar;
int readLength = 0; 
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
      for (int i = 1; i<=6; i++) {
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
  for (int i = 1; i<=6; i++) {
    runMotor(i,0,0); 
  }
  Serial.println("\nStopping All Motors");
}
