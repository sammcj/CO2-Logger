import serial


# Default for macOS, Linux is /dev/ttyUSB
defaultPort = '/dev/tty.SLAB_USBtoUART'


class MHZ14Reader:
    """
    Simple sensor communication class.
    Be _very_ careful using the zero (400ppm) calibration method providedto avoid accidental sensor misconfiguration!

    https://www.google.com/#q=MH-Z14+datasheet+pdf

    # Possible commands


    # mhzCmdReadPPM[9] = [0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]
    # mhzCmdCalibrateZero[9] = [0xFF, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78] # Run in 400ppm or less for 20mins
    # mhzCmdABCEnable[9] = [0xFF, 0x01, 0x79, 0xA0, 0x00, 0x00, 0x00, 0x00, 0xE6]
    # mhzCmdABCDisable[9] = [0xFF, 0x01, 0x79, 0x00, 0x00, 0x00, 0x00, 0x00, 0x86]
    # mhzCmdReset[9] = [0xFF, 0x01, 0x8d, 0x00, 0x00, 0x00, 0x00, 0x00, 0x72]
    # mhzCmdMeasurementRange1000[9] = [0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, 0x03, 0xE8, 0x7B]
    # mhzCmdMeasurementRange2000[9] = [0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, 0x07, 0xD0, 0x8F]
    # mhzCmdMeasurementRange3000[9] = [0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, 0x0B, 0xB8, 0xA3]
    # mhzCmdMeasurementRange5000[9] = [0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, 0x13, 0x88, 0xCB]

    # Run Zero Point (400ppm) calibration, run this for 20mins + in <400ppm Environment
    #_sensorCommand = [0xFF, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78]

    # Enable ABC, run with --single
    #_sensorCommand = [0xFF, 0x01, 0x79, 0xA0, 0x00, 0x00, 0x00, 0x00, 0xE6]

    # Disable ABC, run with --single
    # _sensorCommand = [0xFF, 0x01, 0x79, 0x00, 0x00, 0x00, 0x00, 0x00, 0x86]

    # Default operation, read Co2 levels
    # _sensorCommand = [0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]
    """

    def __init__(self, port, _sensorCommand, open_connection=True):
        """
        :param string port: path to tty
        :param bool open_connection: should port be opened immediately
        """
        self._sensorCommand = _sensorCommand
        self.port = port
        """TTY name"""
        self.link = None
        """Connection with sensor"""
        if open_connection:
            self.connect()

    def connect(self):
        """
        Open tty connection to sensor
        """
        if self.link is not None:
            self.disconnect()
        self.link = serial.Serial(self.port, 9600, bytesize=serial.EIGHTBITS,
                                  parity=serial.PARITY_NONE,
                                  stopbits=serial.STOPBITS_ONE, dsrdtr=True,
                                  timeout=5, interCharTimeout=0.1)

    def disconnect(self):
        """
        Terminate sensor connection
        """
        if self.link:
            self.link.close()

    def _send_data_request(self):
        """
        Send data request control sequence
        """
        self.link.write(bytearray(self._sensorCommand))

    def get_status(self):
        """
        Read data from sensor
        :return {ppa, t}|None:
        """
        self._send_data_request()
        response = self.link.read(9)
        if len(response) == 9:
            return {
                "ppa": response[2] * 0xff + response[3],
                "t": response[4],
            }
        return None


if __name__ == "__main__":
    import time
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='Read data from MH-Z14 CO2 sensor.'
    )
    parser.add_argument('--tty', default=defaultPort, help='tty port to connect',
                        type=str, nargs='?')
    parser.add_argument('--timeout', default=10, help='timeout between requests',
                        type=int, nargs='?')
    parser.add_argument('--command', default='0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79',
                        help='See readme, defaults to reading Co2 PPM', type=str, nargs='?')
    parser.add_argument('--single', action='store_true', help='single measure')
    parser.add_argument('--quit', '-q', action='store_true', help='Check sensor connectivity and quit')
    args = parser.parse_args()
    port = args.tty
    timeout = args.timeout
    _sensorCommand = bytearray([int(x, 16) for x in args.command.split(', ')])

    if args.single:
        timeout = 0

    conn = MHZ14Reader(port, _sensorCommand)
    if not args.quit:
        sys.stderr.write("Connected to {}\n".format(conn.link.name))
    while True:
        status = conn.get_status()
        if status:
            print(
                "{}\t{}\t{}".format(
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    status["ppa"],
                    status["t"]
                )
            )
        else:
            print("No data received")
        sys.stdout.flush()
        if timeout != 0:
            time.sleep(timeout)
        else:
            break
    conn.disconnect()
