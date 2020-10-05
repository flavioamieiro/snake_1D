"""
Snake Game in 1 dimension using fadecandy and a LED strip
Copyright (C) 2020 Flávio Amieiro <amieiro.flavio@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import random
import termios
import time
import tty
import select
import sys

import opclib


NUM_LEDS = 64
TIMEOUT = 0.08


class LEDStrip(list):
    def __init__(self, client, num_leds):
        self.num_leds = num_leds
        self.client = client
        for i in range(self.num_leds):
            self.append((0, 0, 0))

    def append(self, item):
        if len(self) >= self.num_leds:
            raise IndexError("Cannot add more pixels")
        return super().append(item)

    def reset(self):
        self.set_solid_color((0, 0, 0))

    def set_solid_color(self, color):
        for i in range(self.num_leds):
            self[i] = color

    def display(self):
        return self.client.put_pixels(self)


class Snake:

    color = (128, 128, 0)
    velocity = 1

    def __init__(self, led_strip, pos):
        self.led_strip = led_strip
        self.length = 1
        self.pos = pos

    def draw(self):
        for i in range(self.length):
            if self.is_moving_right:
                if self.pos - i > 0:
                    self.led_strip[self.pos - i] = self.color
            else:
                if self.pos + 1 < len(self.led_strip):
                    self.led_strip[self.pos + i] = self.color

    @property
    def is_moving_right(self):
        return self.velocity >= 0

    @property
    def tail(self):
        if self.is_moving_right:
            return self.pos - self.length
        else:
            return self.pos + self.length

    def crash(self):
        self.velocity = 0
        self.color = (128, 0, 0)

    @property
    def crashed(self):
        return not (0 < self.pos < len(self.led_strip) - 1)

    def flip(self):
        if self.is_moving_right:
            self.pos = self.pos - self.length
        else:
            self.pos = self.pos + self.length
        self.velocity = self.velocity * -1

    def grow(self):
        self.length += 1

    def update(self):
        next_pos = self.pos + self.velocity
        if next_pos == (len(self.led_strip) - 1) or next_pos <= 0:
            self.crash()
        self.pos = next_pos


class Fruit:
    color = (0, 128, 0)

    def __init__(self, led_strip, pos=None):
        self.led_strip = led_strip

        if pos is None:
            self.pos = random.randint(1, len(self.led_strip) - 2)
        else:
            self.pos = pos

    def draw(self):
        self.led_strip[self.pos] = self.color


class Game(object):
    timeout_step = 0.0015
    timeout_limit = 0
    _old_velocity = None

    def __init__(self):
        self.opc_client = opclib.opc.Client("localhost:7890")
        self.opc_client.set_interpolation(True)
        self.led_strip = LEDStrip(self.opc_client, NUM_LEDS)
        self.snake = Snake(self.led_strip, 1)

        self.timeout = TIMEOUT
        self.fruit = Fruit(self.led_strip)
        self.level = 1
        self.paused = False

    def read_key(self):
        """
        Read a key from stdin without having to press enter. This
        means putting the tty in Raw mode, and then setting it back to
        it's original state so we can print stuff out without problems.

        man 3 termios has more details on how this works.

        We're also using select (man 3 select) so we can set a timeout
        for how long we'll wait for stdin.

        Taken directly from https://github.com/flavioamieiro/snake_game
        """
        old_tty_attr = termios.tcgetattr(sys.stdin)

        tty.setraw(sys.stdin)

        try:
            inpt, outpt, excpt = select.select([sys.stdin], [], [], self.timeout)

            if inpt:
                key = inpt[0].read(1)
            else:
                key = "?"
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty_attr)

        return key

    @property
    def snake_hits_the_fruit(self):
        return self.snake.pos == self.fruit.pos

    def get_fruit_in_position_that_does_not_overlap_with_snake(self):
        snake_left = min(self.snake.pos, self.snake.tail)
        snake_right = max(self.snake.pos, self.snake.tail)
        positions_ocuppied_by_snake = range(snake_left, snake_right)
        new_fruit_pos = random.choice(
            [
                x
                for x in range(1, len(self.led_strip) - 2)
                if x not in positions_ocuppied_by_snake
            ]
        )
        return Fruit(self.led_strip, new_fruit_pos)

    def draw_walls(self):
        self.led_strip[0] = (64, 64, 64)
        self.led_strip[-1] = (64, 64, 64)

    def toggle_pause(self):
        if self.paused:
            self.snake.velocity = self._old_velocity
            self.paused = False
        else:
            self._old_velocity = self.snake.velocity
            self.snake.velocity = 0
            self.paused = True

    def draw(self):
        self.led_strip.reset()
        self.draw_walls()
        self.fruit.draw()
        self.snake.draw()
        self.led_strip.display()

    def level_up(self):
        self.fruit = self.get_fruit_in_position_that_does_not_overlap_with_snake()
        new_timeout = self.timeout - self.timeout_step
        self.timeout = max(self.timeout_limit, new_timeout)
        self.snake.grow()
        self.level += 1
        print(f"Level {self.level}!")

    def game_over(self):
        red = (128, 0, 0)
        self.led_strip.reset()
        for i in range(len(self.led_strip)):
            self.led_strip[i] = red
            self.led_strip.display()
            time.sleep(0.01)
        self.led_strip.reset()
        self.led_strip.display()
        time.sleep(0.1)
        self.led_strip.set_solid_color(red)
        self.led_strip.display()
        time.sleep(0.1)
        self.led_strip.set_solid_color(red)
        self.led_strip.display()
        time.sleep(0.1)
        print("Game Over :(")

    def won_game(self):
        green = (0, 128, 0)
        self.led_strip.reset()
        for i in range(len(self.led_strip)):
            self.led_strip[i] = green
            self.led_strip.display()
            time.sleep(0.01)
        self.led_strip.reset()
        self.led_strip.display()
        time.sleep(0.1)
        self.led_strip.set_solid_color(green)
        self.led_strip.display()
        time.sleep(0.1)
        self.led_strip.set_solid_color(green)
        self.led_strip.display()
        time.sleep(0.1)
        print("You won the game :)")

    def play(self):
        while True:
            key = self.read_key()

            if key == "q":
                print("Bye!")
                break

            if key == "p":
                self.toggle_pause()

            if key == " ":
                self.snake.flip()
                time.sleep(self.timeout)

            self.snake.update()

            self.draw()


            if self.snake.crashed:
                self.game_over()
                break

            if self.snake.length == len(self.led_strip) - 2:
                self.won_game()
                break

            if self.snake_hits_the_fruit:
                self.level_up()


game = Game()

if __name__ == "__main__":
    try:
        game.play()
    except KeyboardInterrupt:
        print("bye!")
    finally:
        game.led_strip.reset()
        game.led_strip.display()
