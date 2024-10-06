#include<Servo.h>

  Servo top;
  Servo middle;
  Servo bottom;
  int charnum = 0;


void setup() {
  Serial.begin(9600);
  pinMode(2,OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);

  int HH=180;
  int HL=120;
  int LH=60;
  int LL=0;

  top.attach(3);
  middle.attach(5);
  bottom.attach(7);

}

void loop() {

  delay(2000);
  
  String alphabetnum = "abcdefghijklmnopqrstuvwxyz";
 int HH=144;
  int HL=108;
  int LH=72;
  int LL=36;

    

    if (Serial.available()) 
    {
     
      char ch = Serial.read();
  
    //   char ch = alphabetnum.charAt(charnum);
    //   charnum++;
     
     switch(ch){

       case ('a'):
            top.write(HL);
            middle.write(LL);
            bottom.write(LL);
            
            break;

        case ('b'):
            top.write(HL);
            middle.write(HL);
            bottom.write(LL);
            break;

        case ('c'):
            top.write(HH);
            middle.write(LL);
            bottom.write(LL);
            break;
        case ('d'):
            top.write(HH);
            middle.write(LH);
            bottom.write(LL);
            break;
        case ('e'):
            top.write(HL);
            middle.write(LH);
            bottom.write(LL);
            break;
        case ('f'):
            top.write(HH);
            middle.write(HL);
            bottom.write(LL);
            break;
        case ('g'):
            top.write(HH);
            middle.write(HH);
            bottom.write(LL);
            break;
        case ('h'):
            top.write(HL);
            middle.write(HH);
            bottom.write(LL);
            break;
        case ('i'):
            top.write(LH);
            middle.write(HL);
            bottom.write(LL);
            break;
        case ('j' || '0'):
            top.write(LH);
            middle.write(HH);
            bottom.write(LL);
            break;
        case 'k':
            top.write(HL);
            middle.write(LL);
            bottom.write(HL);
            break;
        case 'l':
            top.write(HL);
            middle.write(HL);
            bottom.write(HL);
            break;
        case 'm':
            top.write(HH);
            middle.write(LL);
            bottom.write(HL);
            break;
        case 'n':
            top.write(HH);
            middle.write(LH);
            bottom.write(HL);
            break;
        case 'o':
            top.write(HL);
            middle.write(LH);
            bottom.write(HL);
            break;
        case 'p':
            top.write(HH);
            middle.write(HL);
            bottom.write(HL);
            break;
        case 'q':
            top.write(HH);
            middle.write(HH);
            bottom.write(HL);
            break;
        case 'r':
            top.write(HL);
            middle.write(HH);
            bottom.write(HL);
            break;
        case 's':
            top.write(LH);
            middle.write(HL);
            bottom.write(HL);
            break;
        case 't':
            top.write(LH);
            middle.write(HH);
            bottom.write(HL);
            break;
        case 'u':
            top.write(HL);
            middle.write(LL);
            bottom.write(HH);
            break;
        case 'v':
            top.write(HL);
            middle.write(HL);
            bottom.write(HH);
            break;
        case 'w':
            top.write(LH);
            middle.write(HH);
            bottom.write(LH);
            break;
        case 'x':
            top.write(HH);
            middle.write(LL);
            bottom.write(HH);
            break;
        case 'y':
            top.write(HH);
            middle.write(LH);
            bottom.write(HH);
            break;
        case 'z':
            top.write(HL);
            middle.write(LH);
            bottom.write(HH);
            break;
        default:
            // Turn off all motors for unknown characters 
            top.write(LL);
            middle.write(LL);
            bottom.write(LL);
    }
   }
  }