/*
  ReadAnalogVoltage

  Reads an analog input on pin 0, converts it to voltage, and prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/ReadAnalogVoltage
*/
int LMT86_1 = A0;
int LMT86_2 = A1;
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(LMT86_1,INPUT);
  pinMode(LMT86_2,INPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int LMT86_1_data = analogRead(LMT86_1);
  int LMT86_2_data = analogRead(LMT86_2);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  double voltage_1 = LMT86_1_data * (3000 / 1023.0);
  double voltage_2 = LMT86_2_data * (3000 / 1023.0);
   voltage_1 = map(voltage_1, 0,3000,-50,123);
   voltage_2 = map(voltage_2, 0,3000,-50,123);
  // print out the value you read:
//  float data = voltage_1 + "," + voltage_2 ;
  
//  Serial.print("voltage_1");
  Serial.println(String(voltage_1)+"," +String(voltage_2));
  delay(10);
//Serial.println(voltage_1 + "," + voltage_2);
//  Serial.print(",");
//  Serial.println(voltage_2);
}
