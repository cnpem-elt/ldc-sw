# coding utf-8
# SCPI Commands

class SCPI:
    def __init__(self, instrument_id):
        import pyvisa as visa
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.open_resource(instrument_id)
        print('SCPI Commands enabled!\nInstrument connected successfully!')

    def set_voltage(self, voltage):
        self.instrument.write(':SOURce1:FUNCtion:MODE %s' % 'VOLTage')
        self.instrument.write(':SOURce1:CURRent:LEVel:IMMediate:AMPLitude %G' % voltage)
        print("The source voltage is set to %.3fV" % voltage)
        voltage_value = self.instrument.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        print("Output Voltage: %.3fV" % voltage_value[0])

    def set_current(self, current):
        self.instrument.write(':SOURce1:FUNCtion:MODE %s' % 'CURRent')
        self.instrument.write(':SOURce1:CURRent:LEVel:IMMediate:AMPLitude %G' % current)
        print("The source current is set to %.3fA" % current)
        current_value = self.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        print("Output Current: %.3fA" % current_value[0])

    def enable_output(self):
        self.instrument.write(':OUTPut1:STATe %d' % 1)
        print("Output enabled successfully!")

    def disable_output(self):
        self.instrument.write(':OUTPut1:STATe %d' % 0)
        print("Output disabled successfully!")

    def measure_all(self):
        voltage_value = self.instrument.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        current_value = self.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        print("Output Voltage: %.3fV\nOutput Current: %.3fA" % (voltage_value[0], current_value[0]))

    def measure_current(self):
        current_value = self.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        print("Output Current: %.3fA" % current_value[0])

    def measure_voltage(self):
        voltage_value = self.instrument.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        print("Output Voltage: %.3fV" % voltage_value[0])
