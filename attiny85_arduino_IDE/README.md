Code to run the 1D Snake Game in an ATtiny85 microcrontroler.

It was written in the arduino IDE using
[ATTinyCore](https://github.com/SpenceKonde/ATTinyCore). Please refer
to [their
documentation](https://github.com/SpenceKonde/ATTinyCore#readme) for
installation/programming instructions.

You can refer to the [hardware design files](../hardware/) to see what
you need to hookup to the microcrontroler. If you only want to test it
out, you might get away with only 5V between `Vcc` and `GND`, the
pushbutton on `PB4` and the LED strip's `Din` on `PB3`, but please be
aware that I didn't implement any debouncing in software, so the
button might be very bouncy.
