const int mp1 = 2;
const int mp2 = 3;

void close(int pwm);
void open(int pwm);
void stop(void);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

//char inString[20];
char inChar;
int i = 0;
int readLength = 0; 
int pwm1 = 0;
int tempPWM = 0;

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    readLength = Serial.available();
    if (readLength == 2) {
      // Read inputs and process
      String inString = "";
      for (int x = 0; x<readLength; x++) {
        inChar = Serial.read();
        inString += inChar;
      }
      Serial.print(inString);
      pwm1 = inString.toInt();
      if (pwm1 > 50) { 
        tempPWM = map(pwm1, 50, 100, 0, 255);
        open(tempPWM);
      }
      else if (pwm1 < 50) { 
        tempPWM = map(pwm1, 50, 0, 0, 255);
        close(tempPWM);
      }
      else {
        stop();
      }
    }
  }
//  delay(2000);
  
}

void close(int pwm){
  analogWrite(mp1, pwm);
  analogWrite(mp2, 0);
}

void open(int pwm){
  analogWrite(mp1, 0);
  analogWrite(mp2, pwm);
}
void stop(void){
  analogWrite(mp1, 0);
  analogWrite(mp2, 0);
}
