void grow_snake() {
  snake.len += 1;
}

void flip_snake() {
  int current = millis();
  if (current - last_flip > timeout) {
    if (snake.velocity > 0) {
      snake.pos = snake.pos - snake.len;
    } else {
      snake.pos = snake.pos + snake.len;
    }
    snake.velocity *= -1;
    last_flip = current;
  }
}

void update_snake() {
  snake.pos += snake.velocity;
  if (snake.pos == LED_COUNT - 1 || snake.pos == 0) {
    snake.crashed = true;
  }
}
