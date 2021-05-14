 #include <SoftwareSerial.h>
#include <Servo.h>

Servo servo[7];

int servoCurrentPosition[7]; // current position
int servoPreviousPosition[7]; // previous position
int speedDelay = 15;
String Input="";
int inputAngle[7];
int sizes=1;
int object=1;
// Common servo setup values
int minPulse = 600;   // minimum servo position, us (microseconds)
int maxPulse = 2400;  // maximum servo position, us

void software_Reset()
{
  asm volatile ("  jmp 0");  
} 

void Sizes(int sizes)
{
  if(sizes==1)
  {
      servoCurrentPosition[1] = 142;
      servoCurrentPosition[2] = 148;
      servoCurrentPosition[3] = 136;
      servoCurrentPosition[4] = 70;
      servoCurrentPosition[5] = 165;
      servoCurrentPosition[6] = 115;
  }
  else if(sizes==2)
  {
	servoCurrentPosition[1] = 132;
	servoCurrentPosition[2] = 128;
	servoCurrentPosition[3] = 111;
	servoCurrentPosition[4] = 70;
	servoCurrentPosition[5] = 165;
	servoCurrentPosition[6] = 115;
    
  }
  else
  {
        servoCurrentPosition[1] = 121;
        servoCurrentPosition[2] = 100;
        servoCurrentPosition[3] = 71;
        servoCurrentPosition[4] = 70;
        servoCurrentPosition[5] = 165;
        servoCurrentPosition[6] = 115;
  }
}

void ServoPositionSetting(int NumOfServo)
{
  if (servoPreviousPosition[NumOfServo] > servoCurrentPosition[NumOfServo])
  {
    for ( int j = servoPreviousPosition[NumOfServo]; j >= servoCurrentPosition[NumOfServo]; j--)
    {
      servo[NumOfServo].write(j);
      delay(speedDelay);
  }
  }
  if (servoPreviousPosition[NumOfServo] < servoCurrentPosition[NumOfServo])
  {
    for ( int j = servoPreviousPosition[NumOfServo]; j <= servoCurrentPosition[NumOfServo]; j++)
    {
     servo[NumOfServo].write(j);
      delay(speedDelay);
    }
  }
  servoPreviousPosition[NumOfServo] = servoCurrentPosition[NumOfServo];
}

void CatchAndPut(int sizes)
{
  // catch
  if(object==1 && sizes ==1)
  {
    servoCurrentPosition[6] = 28;
  }
  else if(object==1 && sizes ==2)
  {
    servoCurrentPosition[6] = 25;
  }
  else if(object==1 && sizes ==3)
  {
    servoCurrentPosition[6] = 21;
  }
  else if(object==2 && sizes ==1)
  {
    servoCurrentPosition[6] = 38;
  }
  else if(object==2 && sizes ==2)
  {
    servoCurrentPosition[6] = 35;
  }
  else
  {
    servoCurrentPosition[6] = 33;
  }
  
  ServoPositionSetting(6);

  // up
  servoCurrentPosition[2] = 150;
  ServoPositionSetting(2);
   servoCurrentPosition[3] = 50;
  ServoPositionSetting(3);

  // put
  Sizes(sizes);
  ServoPositionSetting(1);
  ServoPositionSetting(2);
  ServoPositionSetting(3);
  ServoPositionSetting(4);
  ServoPositionSetting(5);
  ServoPositionSetting(6);

  //return
  servoCurrentPosition[1] = 80;
  servoCurrentPosition[2] = 150;
  servoCurrentPosition[3] = 30;
  servoCurrentPosition[4] = 70;
  servoCurrentPosition[5] = 110;
  servoCurrentPosition[6] = 90;

   ServoPositionSetting(2);
  ServoPositionSetting(3);
  ServoPositionSetting(4);
  ServoPositionSetting(5);
  ServoPositionSetting(1);
  ServoPositionSetting(6);
}

void setup()
{
  servo[1].attach(2, minPulse, maxPulse );
  servo[2].attach(3, minPulse, maxPulse );
  servo[3].attach(4, minPulse, maxPulse );
  servo[4].attach(5, minPulse, maxPulse );
  servo[5].attach(6, minPulse, maxPulse );
  servo[6].attach(7, minPulse, maxPulse );

  Serial.begin(2000000); // set the baud rate

  Serial.setTimeout(1);
  delay(speedDelay);

  // Robot arm initial position
  servoPreviousPosition[1] = 80;
  servo[1].write(servoPreviousPosition[1]);
  servoPreviousPosition[2] = 150;
  servo[2].write(servoPreviousPosition[2]);
  servoPreviousPosition[3] = 30;
  servo[3].write(servoPreviousPosition[3]);
  servoPreviousPosition[4] = 70;
  servo[4].write(servoPreviousPosition[4]);
  servoPreviousPosition[5] = 110;
  servo[5].write(servoPreviousPosition[5]);
  servoPreviousPosition[6] =25;
  servo[6].write(servoPreviousPosition[6]);
}

void loop()
{
  // Check for incoming data
  if (Serial.available() > 0)
  {

    Input="";
    Input = Serial.readString();// Read the data as string
    inputAngle[1] =  Input.substring(0, 3).toInt();  // Read the data as string
    inputAngle[2] =  Input.substring(3, 6).toInt();
    inputAngle[3] =  Input.substring(6,9).toInt();
    inputAngle[4] =  Input.substring(9, 12).toInt();
    inputAngle[5] =  Input.substring(12, 15).toInt();
    inputAngle[6] =  Input.substring(15, 18).toInt();
    sizes =  Input.substring(18, 19).toInt();
    object =  Input.substring(19, 20).toInt();
     /*
      Serial.print(Input);
      Serial.print("\n");
      Serial.print(inputAngle[1] );
      Serial.print("\n");
      delay(1);
      Serial.print(inputAngle[2] );
      Serial.print("\n");
      delay(1);
      Serial.print(inputAngle[3] );
      Serial.print("\n");
      Serial.print(inputAngle[4] );
      Serial.print("\n");
      delay(1);
      Serial.print(inputAngle[5] );
      Serial.print("\n");
      delay(1);
      Serial.print(inputAngle[6] );
      Serial.print("\n");
      delay(1);
      Serial.print(sizes );
      Serial.print("\n");
      delay(1);*/
      
      servoCurrentPosition[1] =  inputAngle[1];
      servoCurrentPosition[2] =  inputAngle[2];
      servoCurrentPosition[3] =  inputAngle[3];
      servoCurrentPosition[4] =  inputAngle[4];
      servoCurrentPosition[5] =  inputAngle[5];
      servoCurrentPosition[6] =  inputAngle[6];
      
      ServoPositionSetting(6);
      ServoPositionSetting(1);
      ServoPositionSetting(5);
      ServoPositionSetting(4);
      ServoPositionSetting(3);
      ServoPositionSetting(2);
      CatchAndPut(sizes);
      Serial.print("Sucessful");
    }
  }
