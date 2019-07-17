"""
End stop for informing the stage when it has reached the end of its travel
"""
from logging import getLogger

from linearstage.gpio.base import GpioBase

_LOGGER = getLogger("end stop")


class EndStop:
    """
    An end stop switch that triggers when the stage comes into contact

    Args:
        pin (int): the digital pin/channel that the stop is wired to
        active_low (bool): designates the voltage level when the end stop is 
            activated eg. active_low=True implies the signal is normally high
            (logic 0) and will go low when triggered (logic 1).
        gpio (GpioBase): the gpio interface object
    """
    # pylint: disable=too-few-public-methods
    def __init__(
            self,
            pin: int,
            active_low: bool,
            gpio: GpioBase):
        self._gpio = gpio
        self._pin = pin
        self._callbacks = []
        self._gpio.initialise_input(
            pin, active_low, event_callback=self._handle_triggered_event)
        _LOGGER.info(
            "Initialised end stop %r, pin %d, active-%s",
            self,
            pin,
            "low" if active_low else "high")

    @property
    def pin(self):
        """
        The pin with which the end stop is registered

        Returns:
            int: the pin index
        """
        return self._pin

    @property
    def triggered(self):
        """
        The state of the end stop

        Returns:
            bool: True if the end stop is triggered at this instant
        """
        result = self._gpio.input_triggered(self._pin)
        _LOGGER.debug("End stop %r triggered: %r", self, result)
        return result

    def register_callback(self, callback):
        """
        Register a callback to be called when the endstop is triggered.

        Args:
            callback (obj): the function to be registered
        """
        self._callbacks.append(callback)

    def deregister_callback(self, callback):
        """
        Deregister the given callback

        Args:
            callback (obj): the function to be deregistered
        """
        self._callbacks.remove(callback)

    def _handle_triggered_event(self):
        for callback in self._callbacks:
            callback()