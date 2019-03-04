#include "LowPower.h"

int Pi_off = 2;
int Pi_on = 3;

void setup(void)
{
  pinMode(Pi_on, OUTPUT); 
  pinMode(Pi_off, OUTPUT); 
  pinMode(LED_BUILTIN, OUTPUT);

  // ensure pi is off
  digitalWrite(Pi_on, LOW);
  digitalWrite(Pi_off, HIGH);
  delay(100);
  digitalWrite(Pi_off, LOW);
  
  for(int i = 0; i < 3; i++){
   digitalWrite(LED_BUILTIN, HIGH);
   delay(400);
   digitalWrite(LED_BUILTIN, LOW);
   delay(100);
  }
}

void loop(void) {

  // turn pi on
  digitalWrite(Pi_on, HIGH);
  delay(500);
  digitalWrite(Pi_on, LOW);
  
  for (int i = 1; i <= 9; i++){
    LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
  }

  // turn pi off
  digitalWrite(Pi_off, HIGH);
  delay(100);
  digitalWrite(Pi_off, LOW);

  for (int i = 1; i <= 15; i++){
    LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  }
    
}

