RPiControlBlock
===============

This Python package provides easy access to [petrockblock's ControlBlock](https://controlblock.petrockblock.com). It is
intended for the use on a Raspberry Pi.

Provided Functions
------------------

As a quick overview, the module provides the following functions. Refer to the module documentation for details:

 - open
 - close
 - set_pullup_mode
 - set_direction
 - digital_read
 - digital_write

Installation
------------

If not already done, you need to install PIP via::

    sudo apt-get install python-dev python-pip

Install from `PyPI <https://pypi.python.org/pypi/RPiMCP23S17>`_::

    pip install RPiControlBlock

Example
-------

The following demo periodically toggles all pins of two MCP23S17 components::

    from RPiControlBlock.ControlBlock import ControlBlock
    import time

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

