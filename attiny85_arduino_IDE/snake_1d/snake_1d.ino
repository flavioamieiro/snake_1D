// 1D Snake Game running on an ATTiny85
// Copyright (C) 2020 Flávio Amieiro <amieiro.flavio@gmail.com>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

#include <Adafruit_NeoPixel.h>
#include <avr/power.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#define DEBUG false

#define DEBUG_PIN 1
#define BUTTON_PIN 4
#define LED_PIN 3
#define LED_COUNT 64

#define INITIAL_TIMEOUT 200
#define TIMEOUT_STEP 30
#define TIMEOUT_LIMIT 50

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_KHZ800 + NEO_GRB);

struct Snake {
  unsigned int pos;
  unsigned int len;
  int velocity;
  bool crashed;
  uint32_t color;
};

struct Fruit {
  unsigned int pos;
  uint32_t color;
};

struct Snake snake;

struct Fruit fruit;

unsigned int timeout;
int last_flip;
unsigned int level;

#if DEBUG
bool debug_state = true;
void debug() {
  debug_state = !debug_state;
  digitalWrite(DEBUG_PIN, debug_state);
}
#endif

ISR(PCINT0_vect) {
  if (digitalRead(BUTTON_PIN) == HIGH) {
    flip_snake();
    #if DEBUG
    debug();
    #endif
  }
}


static inline void initInterrupt(void)
{
  GIMSK |= (1 << PCIE);    // pin change interrupt enable
  PCMSK |= (1 << PCINT4 ); // pin change interrupt enabled for PCINT4
  sei();                   // enable interrupts
}


void setup() {
  clock_prescale_set(clock_div_1);

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  initInterrupt();
  reset();
  timeout = INITIAL_TIMEOUT;

  #if DEBUG
  pinMode(DEBUG_PIN, OUTPUT);
  digitalWrite(DEBUG_PIN, debug_state);
  #endif
}

void loop() {
  update_snake();
  draw();

  if (snake.crashed) {
    game_over();
  }
  if (level == 50) {
    won_game();
  }
  if (snake_hits_fruit()) {
    level_up();
  }

  delay(timeout);
}
