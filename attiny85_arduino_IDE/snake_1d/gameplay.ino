bool invalid_fruit_pos(int new_pos) {
  if (snake.velocity > 0) {
    return new_pos >= (snake.pos - snake.len) && new_pos <= snake.pos;
  } else {
    return new_pos >= snake.pos && new_pos <= (snake.pos + snake.len);
  }
};

Fruit get_new_fruit() {
  int new_pos;
  do {
    new_pos = random(1, LED_COUNT - 2);
  } while(invalid_fruit_pos(new_pos));

  struct Fruit new_fruit = {
    .pos = new_pos,
    .color = strip.Color(0, 128, 0)
  };
  return new_fruit;
}

bool snake_hits_fruit() {
  return snake.pos == fruit.pos;
}

void level_up() {
  fruit = get_new_fruit();
  int new_timeout = timeout - TIMEOUT_STEP;
  timeout = max(TIMEOUT_LIMIT, new_timeout);
  grow_snake();
  level += 1;
  Serial.print("Level: ");
  Serial.println(level);
}

void game_over() {
  uint32_t red = strip.Color(128, 0, 0);
  end_animation(red);
  reset();
  delay(2000);
}

void won_game() {
  uint32_t green = strip.Color(0, 128, 0);
  end_animation(green);
  reset();
  delay(2000);
}

void reset() {
  snake = {
    .pos = random(10, LED_COUNT - 12),
    .len = 1,
    .velocity = 1,
    .crashed = false,
    .color = strip.Color(128, 128, 0)
  };

  fruit = get_new_fruit();

  timeout = INITIAL_TIMEOUT;
  last_flip = 0;
  level = 1;
}
