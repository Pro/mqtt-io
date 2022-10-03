"""
Horter & Kalb i2c analog to digital converter
https://www.horter.de/blog/i2c-analog-input-8-kanaele-0-10v-10-bit-2/
"""

from typing import cast

from ...types import CerberusSchemaType, ConfigType, SensorValueType
from . import GenericSensor

REQUIREMENTS = ("smbus2",)
CONFIG_SCHEMA = {
    "i2c_bus_num": {"type": "integer", "required": True, "empty": False},
    "chip_addr": {"type": "integer", "required": True, "empty": False},
}


class Sensor(GenericSensor):
    """
    Implementation of Sensor class for the Adafruit_ADS1x15.
    """

    SENSOR_SCHEMA = {
        "channel": dict(
            type="integer",
            required=True,
            min=0,
            max=7,
        )
    }

    def setup_module(self) -> None:
        # pylint: disable=import-outside-toplevel,attribute-defined-outside-init
        # pylint: disable=import-error,no-member
        from smbus2 import SMBus  # type: ignore

        self.bus = SMBus(self.config["i2c_bus_num"])
        self.address: int = self.config["chip_addr"]

    def get_value(self, sens_conf: ConfigType) -> SensorValueType:
        """
        Get the temperature, humidity or pressure value from the sensor
        """
        channel = sens_conf["channel"]
        assert 0 <= channel <= 7

        block = self.bus.read_i2c_block_data(self.address, 0, 17)

        # Value is between 0 and max 1023
        val_1023 = block[2 + channel*2] * 265 + block[1 + channel*2]

        # 1023 represents maximum 10V, therefore convert

        return cast(
            float,
            float(val_1023)/1023.0 * 10.0,
        )
