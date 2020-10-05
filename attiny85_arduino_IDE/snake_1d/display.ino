void solid_color(uint32_t color) {
    strip.clear();
    for(int i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i, color);
    }
    strip.show();
}

void end_animation(uint32_t color) {
  strip.clear();
  for(int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, color);
    strip.show();
  };
  strip.clear();
  strip.show();
  delay(100);
  solid_color(color);
  strip.show();
  delay(100);
  solid_color(color);
  strip.show();
  delay(100);
}

void draw_walls() {
  uint32_t wall_color = strip.Color(64, 64, 64);
  strip.setPixelColor(0, wall_color);
  strip.setPixelColor(LED_COUNT-1, wall_color);
}

void draw_fruit() {
  strip.setPixelColor(fruit.pos, fruit.color);
}

void draw_snake() {
  for (int i = 0; i < snake.len; i++) {
    if (snake.velocity > 0) {
      if (snake.pos - i > 0) {
        strip.setPixelColor(snake.pos - i, snake.color);
      }
    } else {
      if (snake.pos + i < LED_COUNT - 1) {
        strip.setPixelColor(snake.pos + i, snake.color);
      }
    }
  }
}

void draw() {
  strip.clear();
  draw_walls();
  draw_fruit();
  draw_snake();
  strip.show();
}
