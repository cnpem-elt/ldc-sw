#!/usr/bin/env python3
# SCPI_Commands.py

class SCPI:
    """
    Sets up a series of commands to use with an instrument compatible with SCPI communication
    """
    def __init__(self, instrument_id):
        """
        Connects to the desired instrument to start SCPI communication

        :param instrument_id: ID of the desired instrument
        :type instrument_id: string
        """
        import pyvisa as visa
        rm = visa.ResourceManager()
        self.instrument = rm.open_resource(instrument_id)

    def set_protection_voltage(self, protection_voltage):
        """
        Sets the compliance voltage to the instrument output

        :param protection_voltage: The desired protection voltage
        :type protection_voltage: float

        :return: A float with the actual protection voltage value
        :rtype: float
        """
        self.instrument.write(':SOURce1:FUNCtion:MODE %s' % 'CURRent')
        self.instrument.write(':SENSe1:VOLTage:DC:PROTection:LEVel %G' % protection_voltage)
        protection_value = self.instrument.query_ascii_values(':SENSe:VOLTage:DC:PROTection:LEVel?')
        pvoltage_result = float('{:.3f}'.format(protection_value[0]))
        return pvoltage_result

    def set_protection_current(self, protection_current):
        """
        Sets the compliance current to the instrument output

        :param protection_current: The desired protection current
        :type protection_current: float

        :return: A float with the actual protection current value
        :rtype: float
        """
        self.instrument.write(':SOURce1:FUNCtion:MODE %s' % 'VOLTage')
        self.instrument.write(':SENSe:CURRent:DC:PROTection:LEVel %G' % protection_current)
        protection_value = self.instrument.query_ascii_values(':SENSe:CURRent:DC:PROTection:LEVel?')
        pcurrent_result = float('{:.3f}'.format(protection_value[0]))
        return pcurrent_result

    def set_voltage(self, voltage):
        """
        Sets a voltage value to the instrument output

        :param voltage: The desired value in Volts
        :type voltage: float

        :return: A float with the actual output voltage value
        :rtype: float
        """
        self.instrument.write(':SOURce1:FUNCtion:MODE %s' % 'VOLTage')
        self.instrument.write(':SOURce1:CURRent:LEVel:IMMediate:AMPLitude %G' % voltage)
        print("The source voltage is set to %.3fV" % voltage)
        voltage_value = self.instrument.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        voltage_result = float('{:.3f}'.format(voltage_value[0]))
        return voltage_result

    def set_current(self, current):
        """
        Sets a current value to the instrument output

        :param current: The desired value in Amperes
        :type current: float

        :return: A string with the actual output current value
        :rtype: float
        """
        self.instrument.write(':SOURce1:FUNCtion:MODE %s' % 'CURRent')
        self.instrument.write(':SOURce1:CURRent:LEVel:IMMediate:AMPLitude %G' % current)
        print("The source current is set to %.3fA" % current)
        current_value = self.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        current_result = float('{:.3f}'.format(current_value[0]))
        return current_result

    def enable_output(self):
        """
        Enables the instrument output

        :return: A string confirming the operation
        :rtype: str
        """
        self.instrument.write(':OUTPut1:STATe %d' % 1)
        return "Output successfully enabled !"

    def disable_output(self):
        """
        Disables the instrument output

        :return: A string confirming the operation
        :rtype: str
        """
        self.instrument.write(':OUTPut1:STATe %d' % 0)
        return "Output successfully disabled!"

    def measure_all(self):
        """
        Print the actual output values for current and voltage

        :return: A string with the actual values
        :rtype: dict
        """
        voltage_value = self.instrument.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        voltage_result = float('{:.3f}'.format(voltage_value[0]))
        current_value = self.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        current_result = float('{:.3f}'.format(current_value[0]))
        values_dict = {
            "voltage": voltage_result,
            "current": current_result
        }
        return values_dict

    def measure_current(self):
        """
        Print the actual output current value

        :return: A float with the actual current value in Amperes
        :rtype: float
        """
        current_value = self.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        current_result = float('{:.3f}'.format(current_value[0]))
        return current_result

    def measure_voltage(self):
        """
        Print the actual output voltage value

        :return: A float with the actual voltage value in Volts
        :rtype: float
        """
        voltage_value = self.instrument.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        voltage_result = float('{:.3f}'.format(voltage_value[0]))
        return voltage_result
