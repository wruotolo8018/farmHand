/* 
 *  MegaMotorDriver Debugger Code
 *  Wilson Ruotolo
 *  3/13/2020
 */

// Setup arrays for motor control pins
int pwmArray[13];
int digArray1[13];
int digArray2[13];

// Function prototypes
void runMotor(int motorSelect, int dir, int pwmVal);
void stopAll();
void closeSequence();
void openSequence();

void setup() {
  // Setup all the pwm pins according to current configuration
  pwmArray[1] = 10;   pwmArray[2] = 11;   pwmArray[3] = 9 ;
  pwmArray[7] = 13;   pwmArray[8] = 12;   pwmArray[9]= 2 ;

  pwmArray[4] = 8 ;   pwmArray[5]  = 6 ;   pwmArray[6] = 7 ;
  pwmArray[10]= 5 ;   pwmArray[11] = 4 ;   pwmArray[12]= 3 ;

  // Setup all the digital direction setting pins according to current configuration  
  // Finger 1
  for (int i = 22; i<53; i++) {
    pinMode(i, OUTPUT);
  }
  
  digArray1[1]  = 50;   digArray2[1]  = 48;
  digArray1[2]  = 46;   digArray2[2]  = 44;
  digArray1[3]  = 51;   digArray2[3]  = 49;  
  // Thumb
  digArray1[7]  = 42;   digArray2[7]  = 40;  
  digArray1[8]  = 38;   digArray2[8]  = 36;
  digArray1[9]  = 28;   digArray2[9]  = 30;
  
  // Finger 2
  digArray1[4]  = 47;   digArray2[4]  = 45; // Working
  digArray1[5]  = 25;   digArray2[5]  = 27; // Working
  digArray1[6]  = 31;   digArray2[6]  = 29; // Working

  // Start serial comms going at a chosen baud rate
  Serial.begin(115200);
}

char inChar;
char inDir = '1';
int readLength = 0; 
int pwm1 = 0;
int mappedPWM = 0;
int curTime = millis();
int prevTime = millis();
int printInterval = 3000;
int pwmValArray[13];
int pwmDirArray[13]; // just for debugging

void loop() {
  if (Serial.available() > 0){
    inChar = Serial.read();
    Serial.read();
//    Serial.print("New Input: ");
//    Serial.print(inChar);
//    Serial.println("");

    if (inChar == ' '){
      stopAll();
    }
    else if (inChar == 'f'){
      inDir = 1;
      Serial.println("Setting direction to forward");
    }
    else if (inChar == 'b'){
      inDir = 0;
      Serial.println("Setting direction to backward");
    }
    else if (inChar == 'c'){
      Serial.println("Closing Hand");
      closeSequence();
    }
    else if (inChar == 'o'){
      Serial.println("Opening Hand");
      openSequence();
    }
    else if (inChar == 'g'){
    }
    else{
      int motorNum = inChar - '0';
      int motorDir = inDir;
      runMotor(motorNum, motorDir, 100);
      
      Serial.print("Running motor ");
      Serial.print(inChar);
      Serial.println("");
    }
  }
  
}

void closeSequence(){
  runMotor(1, 1, 50);
  runMotor(2, 1, 50);
  runMotor(3, 0, 50);
  runMotor(4, 1, 50);
  runMotor(5, 1, 50);
  runMotor(6, 0, 50);
  runMotor(7, 1, 50);
  runMotor(8, 1, 50);
  runMotor(9, 0, 50);
}

void openSequence(){
  runMotor(1, 0, 50);
  runMotor(2, 0, 50);
  runMotor(3, 1, 50);
  runMotor(4, 0, 50);
  runMotor(5, 0, 50);
  runMotor(6, 1, 50);
  runMotor(7, 0, 50);
  runMotor(8, 0, 50);
  runMotor(9, 1, 50);
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
  Serial.println("Stopping All Motors");
}
