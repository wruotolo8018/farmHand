/* 
 *  MegaMotorDriver Debugger Code
 *  Wilson Ruotolo
 *  3/13/2020
 */

// Setup arrays for motor control pins
int pwmArray[13];
int digArray1[13];
int digArray2[13];

int num_motors = 8;

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
  digArray1[5]  = 37;   digArray2[5]  = 39;
  digArray1[6]  = 41;   digArray2[6]  = 43;

  // Finger 4
  pwmArray[7] = 6;   pwmArray[8] = 7;   
  digArray1[7]  = 27;   digArray2[7]  = 29;
  digArray1[8]  = 31;   digArray2[8]  = 33;

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
  for (int i = 1; i<=num_motors; i++) {
    runMotor(i,0,0); 
    Serial.print("Stopping motor ");
    Serial.println(i);
  }
  Serial.println("Stopping All Motors");

//  analogWrite/(0, 0);

  
}
