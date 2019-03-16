#!/usr/bin/python

# Copyright 2016-2019 Florian Mueller (contact@petrockblock.com)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import enum

from RPiMCP23S17.MCP23S17 import *


class ControlBlock(object):
    """This class provides an abstraction of the ControlBlock from
    petrockblock.com
    It depends on the Python package RPiMCP23S17, which is available
    from https://pypi.python.org/pypi/RPi.GPIO/0.5.11 and
    https://pypi.python.org/pypi/spidev.
    """

    class Pin(enum.Enum):
        p1_right = 1
        p1_left = 2
        p1_up = 3
        p1_down = 4
        p1_sw1 = 5
        p1_sw2 = 6
        p1_sw3 = 7
        p1_sw4 = 8
        p1_sw5 = 9
        p1_sw6 = 10
        p1_sw7 = 11
        p1_sw8 = 12
        p1_start = 13
        p1_coin = 14
        p1_a = 15
        p1_b = 16
        p2_right = 17
        p2_left = 18
        p2_up = 19
        p2_down = 20
        p2_sw1 = 21
        p2_sw2 = 22
        p2_sw3 = 23
        p2_sw4 = 24
        p2_sw5 = 25
        p2_sw6 = 26
        p2_sw7 = 27
        p2_sw8 = 28
        p2_start = 29
        p2_coin = 30
        p2_a = 31
        p2_b = 32

    class PullUp(enum.Enum):
        enabled = 0
        disabled = 1

    class Direction(enum.Enum):
        input = 0
        output = 1

    class Level(enum.Enum):
        low = 0
        high = 1

    def __init__(self, sj1=0, sj2=0):
        """
        Constructor
        Initializes all attributes with 0.

        Keyword arguments:
        sj1 -- The value of solder jumper 1. Defaults to 0
        sj2 -- The value of solder jumper 2. Defaults to 0
        """
        self._sj1 = sj1
        self._sj2 = sj2
        self._mcp1 = None
        self._mcp2 = None
        self._isInitialized = False

    def open(self):
        """Initializes the ControlBlock with input direction
        for all pins and enabled pull-up resistors.
        """
        self._mcp1 = MCP23S17(self._sj2 * 4 + self._sj1 * 2)
        self._mcp2 = MCP23S17(self._sj2 * 4 + self._sj1 * 2 + 1)
        self._mcp1.open()
        self._mcp2.open()

        # set defaults to input
        for index in range(0, 15):
            self._mcp1.setDirection(index, MCP23S17.DIR_INPUT)
            self._mcp1.setPullupMode(index, MCP23S17.PULLUP_ENABLED)
            self._mcp2.setDirection(index, MCP23S17.DIR_INPUT)
            self._mcp2.setPullupMode(index, MCP23S17.PULLUP_ENABLED)

        self._isInitialized = True

    def close(self):
        """Closes the SPI connection that the ControlBlock components are using.
        """
        self._mcp1.close()
        self._mcp2.close()
        self._isInitialized = False

    def set_pullup_mode(self, pin: Pin, mode: PullUp):
        """Enables or disables the pull-up mode for a given pin.

        Parameters:
        pin -- The pin to be controlled
        mode -- The pull-up mode (Pullup.disabled, Pullup.enabled)
        """
        assert self._isInitialized, "ControlBlock instance is not initialized"

        switcher = {
            ControlBlock.PullUp.disabled: MCP23S17.PULLUP_DISABLED,
            ControlBlock.PullUp.enabled: MCP23S17.PULLUP_ENABLED
        }
        mcp, index = self._get_mcp_and_index(pin)
        mcp.setPullupMode(index, switcher.get(mode))

    def set_direction(self, pin: Pin, direction: Direction):
        """Sets the direction for a given pin.

        Parameters:
        pin -- The pin to be controlled
        direction -- The direction of the pin (Direction.output, Direction.input)
        """
        assert self._isInitialized, "ControlBlock instance is not initialized"

        switcher = {
            ControlBlock.Direction.output: MCP23S17.DIR_OUTPUT,
            ControlBlock.Direction.input: MCP23S17.DIR_INPUT
        }
        mcp, index = self._get_mcp_and_index(pin)
        mcp.setDirection(index, switcher.get(direction))

    def digital_read(self, pin: Pin) -> Level:
        """Reads the logical level of a given pin.

        Parameters:
        pin -- The pin to be read
        Returns:
         - Level.low, if the logical level of the pin is low,
         - Level.high, otherwise.
        """
        assert self._isInitialized, "ControlBlock instance is not initialized"

        switcher = {
            MCP23S17.LEVEL_HIGH: ControlBlock.Level.high,
            MCP23S17.LEVEL_LOW: ControlBlock.Level.low
        }
        mcp, index = self._get_mcp_and_index(pin)
        level = mcp.digitalRead(index)
        return switcher.get(level)

    def digital_write(self, pin: Pin, level: Level):
        """Sets the level of a given pin.
        Parameters:
        pin -- The pin to be controlled
        level -- The logical level to be set (Level.low, Level.high)
        """
        assert self._isInitialized, "ControlBlock instance is not initialized"

        switcher = {
            ControlBlock.Level.high: MCP23S17.LEVEL_HIGH,
            ControlBlock.Level.low: MCP23S17.LEVEL_LOW
        }
        mcp, index = self._get_mcp_and_index(pin)
        mcp.digitalWrite(index, switcher.get(level))

    def _get_mcp_and_index(self, pin: Pin):
        switcher_mcp = {
            ControlBlock.Pin.p1_right: self._mcp1,
            ControlBlock.Pin.p1_left: self._mcp1,
            ControlBlock.Pin.p1_up: self._mcp1,
            ControlBlock.Pin.p1_down: self._mcp1,
            ControlBlock.Pin.p1_sw1: self._mcp1,
            ControlBlock.Pin.p1_sw2: self._mcp1,
            ControlBlock.Pin.p1_sw3: self._mcp1,
            ControlBlock.Pin.p1_sw4: self._mcp1,
            ControlBlock.Pin.p1_sw5: self._mcp2,
            ControlBlock.Pin.p1_sw6: self._mcp2,
            ControlBlock.Pin.p1_sw7: self._mcp2,
            ControlBlock.Pin.p1_sw8: self._mcp2,
            ControlBlock.Pin.p1_start: self._mcp2,
            ControlBlock.Pin.p1_coin: self._mcp2,
            ControlBlock.Pin.p1_a: self._mcp2,
            ControlBlock.Pin.p1_b: self._mcp2,
            ControlBlock.Pin.p2_right: self._mcp1,
            ControlBlock.Pin.p2_left: self._mcp1,
            ControlBlock.Pin.p2_up: self._mcp1,
            ControlBlock.Pin.p2_down: self._mcp1,
            ControlBlock.Pin.p2_sw1: self._mcp1,
            ControlBlock.Pin.p2_sw2: self._mcp1,
            ControlBlock.Pin.p2_sw3: self._mcp1,
            ControlBlock.Pin.p2_sw4: self._mcp1,
            ControlBlock.Pin.p2_sw5: self._mcp2,
            ControlBlock.Pin.p2_sw6: self._mcp2,
            ControlBlock.Pin.p2_sw7: self._mcp2,
            ControlBlock.Pin.p2_sw8: self._mcp2,
            ControlBlock.Pin.p2_start: self._mcp2,
            ControlBlock.Pin.p2_coin: self._mcp2,
            ControlBlock.Pin.p2_a: self._mcp2,
            ControlBlock.Pin.p2_b: self._mcp2
        }

        switcher_index = {
            ControlBlock.Pin.p1_right: 0,
            ControlBlock.Pin.p1_left: 1,
            ControlBlock.Pin.p1_up: 2,
            ControlBlock.Pin.p1_down: 3,
            ControlBlock.Pin.p1_sw1: 4,
            ControlBlock.Pin.p1_sw2: 5,
            ControlBlock.Pin.p1_sw3: 6,
            ControlBlock.Pin.p1_sw4: 7,
            ControlBlock.Pin.p1_sw5: 0,
            ControlBlock.Pin.p1_sw6: 1,
            ControlBlock.Pin.p1_sw7: 2,
            ControlBlock.Pin.p1_sw8: 3,
            ControlBlock.Pin.p1_start: 4,
            ControlBlock.Pin.p1_coin: 5,
            ControlBlock.Pin.p1_a: 6,
            ControlBlock.Pin.p1_b: 7,
            ControlBlock.Pin.p2_right: 15,
            ControlBlock.Pin.p2_left: 14,
            ControlBlock.Pin.p2_up: 13,
            ControlBlock.Pin.p2_down: 12,
            ControlBlock.Pin.p2_sw1: 11,
            ControlBlock.Pin.p2_sw2: 10,
            ControlBlock.Pin.p2_sw3: 9,
            ControlBlock.Pin.p2_sw4: 8,
            ControlBlock.Pin.p2_sw5: 15,
            ControlBlock.Pin.p2_sw6: 14,
            ControlBlock.Pin.p2_sw7: 13,
            ControlBlock.Pin.p2_sw8: 12,
            ControlBlock.Pin.p2_start: 11,
            ControlBlock.Pin.p2_coin: 10,
            ControlBlock.Pin.p2_a: 9,
            ControlBlock.Pin.p2_b: 8
        }
        return switcher_mcp.get(pin, "Invalid pin"), switcher_index.get(pin, "Invalid pin")


if __name__ == '__main__':
    """The following demo periodically toggles the level of
    all pins of the ControlBlock.
    """

    controlblock: ControlBlock = ControlBlock()
    controlblock.open()

    for pin in ControlBlock.Pin:
        controlblock.set_direction(pin, ControlBlock.Direction.output)

    print("Starting blinky on all pins (CTRL+C to quit)")
    while (True):
        for pin in ControlBlock.Pin:
            controlblock.digital_write(pin, ControlBlock.Level.high)
        time.sleep(1)

        for pin in ControlBlock.Pin:
            controlblock.digital_write(pin, ControlBlock.Level.low)
        time.sleep(1)
