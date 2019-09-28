/*practice*/
char btdata;
int Q,P;
void SetSpeed(int Speed)
{
  analogWrite(11, Speed);//CHECK THE DIGITAL PIN
  analogWrite(10, Speed);
}
void moveForward()
     {
       digitalWrite(2, HIGH); // MOTOR DRIVER1
       digitalWrite(3, LOW);
       digitalWrite(4, HIGH);
       digitalWrite(5, LOW);
       Serial.println("FORWARD");
     }
void moveBackward()
     {
       digitalWrite(2, LOW); // MOTOR DRIVER1
       digitalWrite(3, HIGH);
       digitalWrite(4, LOW);
       digitalWrite(5, HIGH);
       Serial.println("BACKWARD");
     }
void arcFRight()
     {
       digitalWrite(2, HIGH); // MOTOR DRIVER1
       digitalWrite(3, LOW);
       digitalWrite(4, HIGH);
       digitalWrite(5, LOW);
       Serial.println(" ARC FORWARD RIGHT");
     }
void arcBRight()
     {
       digitalWrite(2, LOW); // MOTOR DRIVER1
       digitalWrite(3, HIGH);
       digitalWrite(4, LOW);
       digitalWrite(5, HIGH);
       Serial.println(" ARC BACKWARD RIGHT");       
     }
void arcFLeft()
     {
       digitalWrite(2, LOW); // MOTOR DRIVER1
       digitalWrite(3, LOW);
       digitalWrite(4, LOW);
       digitalWrite(5, LOW);
       Serial.println(" ARC FORWARD LEFT");      
     }
void arcBLeft()
     {
       digitalWrite(2, LOW); // MOTOR DRIVER1
       digitalWrite(3, LOW);
       digitalWrite(4, LOW);
       digitalWrite(5, LOW);
       Serial.println(" ARC BACKWARD LEFT");      
     }
void spotLeft()
     {
       digitalWrite(2, LOW); // MOTOR DRIVER1
       digitalWrite(3, HIGH);
       digitalWrite(4, LOW);
       digitalWrite(5, HIGH);
       Serial.println(" SPOT LEFT");          
     }
void spotRight()
     {
       digitalWrite(2, HIGH); // MOTOR DRIVER1
       digitalWrite(3, LOW);
       digitalWrite(4, HIGH);
       digitalWrite(5, LOW);
       Serial.println(" SPOT RIGHT");      
     }
void Stop()
     {
       digitalWrite(2, LOW); // MOTOR DRIVER1
       digitalWrite(3, LOW);
       digitalWrite(4, LOW);
       digitalWrite(5, LOW);
       Serial.println("-------");      
     }






void setup() {
  // put your setup code here, to run once:
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  Serial.begin(38400); //----------------CHANGE VALUE BASED ON MODEL
}

void loop() 
{
  if(Serial.available()){
    btdata = Serial.read();
  
  if(btdata=='X'){
   String str = Serial.readStringUntil('$');
   Serial.println(str);
   Q=P=str.toInt();
   Serial.println(Q);
   btdata = "";
  }
  else if (btdata == 'F') 
  {
   moveForward();
  analogWrite(11,P);//CHECK THE DIGITAL PIN
  analogWrite(10,Q);
  } 
  else if (btdata == 'B') 
  {
   moveBackward();
  analogWrite(11,P);//CHECK THE DIGITAL PIN
  analogWrite(10,Q);
  } 
  else if (btdata == 'R')
  {
   spotRight();
  analogWrite(11,P);//CHECK THE DIGITAL PIN
  analogWrite(10,Q);
  }
  else if (btdata == 'I') 
  {
   arcFRight();
  analogWrite(11,P);//CHECK THE DIGITAL PIN
  analogWrite(10,Q);
  } 
  else if (btdata == 'L')
  {
  spotLeft();
  analogWrite(11,P);//CHECK THE DIGITAL PIN
  analogWrite(10,Q);
  }
  else if (btdata == 'G') 
  {
   arcFLeft();
  analogWrite(11,P);//CHECK THE DIGITAL PIN
  analogWrite(10,Q);
  }
  else if (btdata == 'S')
  {
   Stop();
  } 
  else 
  {
   Stop();
  }
  }
}
