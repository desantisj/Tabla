//pin_def
#include <Adafruit_NeoPixel.h>

#define PIN 12

#define N_LEDS 60

#define dir_1 7
#define pwm_1 6

#define dir_2 4
#define pwm_2 3

Adafruit_NeoPixel strip (N_LEDS, PIN, NEO_GRB + NEO_KHZ800);

void setup()
{
  pinMode(pwm_1,OUTPUT);
  pinMode(dir_1,OUTPUT);
  pinMode(pwm_2,OUTPUT);
  pinMode(dir_2,OUTPUT);
  strip.begin();
  strip.setBrightness(60);
  Serial.begin(9600);
}

void loop()
{
  String data;
  
  int dir_type_index;
  int dir_type;
  int dir_pin;

  int dir_state_index;
  bool dir_state;

  int pwm_selector_index;
  int pwm_selector;
  int pwm_pin;

  int pwm_signal_index;
  int pwm_signal;

  int side_index;
  int side;

  for(int i =0; i < 61; i++){
        strip.setPixelColor(i, 0, 255, 200);
    }
 
  strip.setBrightness(60);
  strip.show();

  while (Serial.available())
  {
    if (Serial.available() > 0)
    {
      data = Serial.readStringUntil('\r');

      dir_type_index = data.indexOf(',');
      dir_type = data.substring(0, dir_type_index).toInt();

      dir_state_index = data.indexOf(',', dir_type_index+1);
      dir_state = (data.substring(dir_type_index+1,dir_state_index)).toInt();

      pwm_selector_index = data.indexOf(',', dir_state_index+1);
      pwm_selector = (data.substring(dir_state_index+1,pwm_selector_index)).toInt();

      pwm_signal_index = data.indexOf(',', pwm_selector_index+1);
      pwm_signal = (data.substring(pwm_selector_index+1,pwm_signal_index)).toInt();

      side_index = data.indexOf(',', pwm_signal_index+1);
      side = (data.substring(pwm_signal_index+1, side_index)).toInt();

      switch (dir_type)
      {
        case 1:
          dir_pin = dir_1;

       
          
          break;

        case 2:
          dir_pin = dir_2;
          
          break;
      }

      switch (pwm_selector)
      {
        case 1:
          pwm_pin = pwm_1;
          
//          if(side == 1){
//            right_on();
//          }
//
//          if(side == 0){
//            right_off();
//          }
          break;

        case 2:
          pwm_pin = pwm_2;
//          if (side == 1){
//            left_on();
//          }
//
//          if(side == 0){
//            left_off();
//          }
//          break;
      }

      run_motor(dir_pin, dir_state, pwm_pin, pwm_signal);
    }
  }  
}

void run_motor(int dir_pin, bool dir_state, int pwm_pin, int pwm_signal)
{
  Serial.println();
  Serial.print(dir_pin);
  Serial.print(" ");
  Serial.print(dir_state);
  Serial.print(" ");
  Serial.print(pwm_pin);
  Serial.print(" ");
  Serial.println(pwm_signal);

  
  
  digitalWrite(dir_pin, dir_state);
  analogWrite(pwm_pin, pwm_signal);
}

//void left_on(){
//  for(int i =40; i < 61; i++){
//      strip.setPixelColor(i, 0, 255, 255);
//  }
// 
//  strip.setBrightness(60);
//
//  strip.show();
//}
//
//void right_on(){
//  
//  for(int i =0; i < 40; i++){
//      strip.setPixelColor(i, 0, 255, 255);
//  }
//  strip.setBrightness(60);
//
//  strip.show();
//
//}
//
//void right_off(){
//  for(int i =0; i < 40; i++){
//      strip.setPixelColor(i, 0, 0, 0);
//  }
//
//  strip.setBrightness(0);
//  strip.show();
//
//}
//
//void left_off(){
//  for(int i =40; i < 61; i++){
//      strip.setPixelColor(i, 0, 0, 0);
//  }
//  
//  strip.setBrightness(0);
//  strip.show();
//
//}
