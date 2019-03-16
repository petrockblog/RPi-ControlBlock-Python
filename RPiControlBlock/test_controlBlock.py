from unittest import TestCase

from RPiControlBlock import ControlBlock


class TestControlBlock(TestCase):
    def test___init__(self):
        controlblock = ControlBlock.ControlBlock()
        self.assertEqual(controlblock._sj1, 0)
        self.assertEqual(controlblock._sj2, 0)

        controlblock = ControlBlock.ControlBlock(sj1=1, sj2=0)
        self.assertEqual(controlblock._sj1, 1)
        self.assertEqual(controlblock._sj2, 0)

        controlblock = ControlBlock.ControlBlock(sj1=0, sj2=1)
        self.assertEqual(controlblock._sj1, 0)
        self.assertEqual(controlblock._sj2, 1)

        controlblock = ControlBlock.ControlBlock(sj1=1, sj2=1)
        self.assertEqual(controlblock._sj1, 1)
        self.assertEqual(controlblock._sj2, 1)

    def test_open(self):
        controlblock = ControlBlock.ControlBlock()
        controlblock.open()
