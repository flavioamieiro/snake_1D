This is a python implementation of the 1D Snake Game using
[fadecandy](https://github.com/scanlime/fadecandy) to control the LED
strip.

The code is basically copied over from [an earlier
implementation](https://github.com/flavioamieiro/snake_game/) and
adapted to use an LED strip for output.

I recommend creating a [virtual
environment](https://docs.python.org/3/tutorial/venv.html) and
installing the requirements with `pip install -r
requirements.txt`. This code was written using python 3.8.2.

Then you need the fadecandy server running on your computer and hook
it up as described in the simple example in [fadecandy's
documentation simple example](https://github.com/scanlime/fadecandy/blob/master/README.md#simple-example):


![Fadecandy system diagram 1](https://raw.github.com/scanlime/fadecandy/master/doc/images/system-diagram-1.png)


After that, just run `python snake_game.py`. The space bar controls the snake.
