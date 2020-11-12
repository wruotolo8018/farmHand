/* 
 *  Basic Futek Sensor Read and Interface
 *  Wilson Ruotolo & Dane Brouwer
 *  11/11/2020
 */

// Setup arrays for motor control pins
const int num_sensors = 2;
int sns_array[num_sensors];
String output_str;

void setup() {  
  Serial.begin(115200);
}

int curTime = millis();
int prevTime = millis();
int readRate = 10; // hz

void loop() {
  curTime = millis();
  output_str = "";

  if (curTime - prevTime > 1000/readRate) {
    // iterate through analog sensors and read values
    for (int i = 0; i < num_sensors; i++) {
      sns_array[i] = analogRead(i);
    }

    // concatenate into transmit message
    for (int i = 0; i < num_sensors; i++) {
      output_str = output_str + String(sns_array[i]) + "_";
    }
    output_str = output_str + String(millis()) + "_\n";
    
    // send over serial
    Serial.print(output_str);

    prevTime = curTime;
  }

}
