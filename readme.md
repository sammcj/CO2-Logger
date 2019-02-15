# Example MH-Z14 / MH-Z19 CO2 sensor reader and visualiser

* Read data from UART(serial)-connected MH-Z14 or MH-Z19 sensor using python.
* visualise received data using html and plotly.js library.

## Screenshot of example data

![plot](https://user-images.githubusercontent.com/862951/52826593-a98a5400-3115-11e9-868a-72a763b6d587.jpg)

## Usage

### Connection

Sensor can be queried using 3.3v UART at 9600 bps. Sensor main feed voltage is 5v.

Can be connected to computer using almost any USB-UART converter if voltage matches.

### Requirements

- Python2 (Python3 support comming)
- `pip2 install serial pyserial`
- A USB -> Serial UART connector or similar

### Querying

```
$ python2 CO2Reader.py /dev/tty.SLAB_USBtoUART 2
Connected to /dev/tty.SLAB_USBtoUART
2019-02-15 11:02:11	463	64
2019-02-15 11:02:13	467	64
2019-02-15 11:02:15	467	64
2019-02-15 11:02:17	470	64
...
```
3 fields separated by tab: timestamp, CO2 concentration (ppm), internal sensor temperature (fahrenheit)
 
Use stream redirection to save data series to file:

```shell
touch example.log
python CO2Reader.py /dev/tty.SLAB_USBtoUART 2 >>example.log
```

#### Options

- `--single` perform a single measurement

### Visualizing

* install npm dependencies `npm install`
* start server `python2 -m SimpleHTTPServer 8088`
* open browser at http://localhost:8088/plot.html - WARNING: Make sure your machine is firewalled or anyone could access the directory
* select your log file in input field

## Technical Specifications MH-Z19


|          Attribute          |            Value            |
|-----------------------------|-----------------------------|
| Target gas                  | Carbon Dioxide CO2          |
| Operating Voltage           | 3.6 to 5.5 Vdc              |
| Operating current           | < 18mA average              |
| Interface levels            | 3.3 Vdc                     |
| Output signal format        | UART or PWM                 |
| Preheat time                | 3 min                       |
| Response time               | <60 s                       |
| Accuracy                    | ± (50 ppm+5% reading value) |
| Measuring range             | 0 to 5000 ppm               |
| Operating temperature range | 0 to + 50°C                 |
| Dimensions                  | 33mm×20mm×9mm(L×W×H)        |


## Wiring

| Function | UART / Signal | MH-Z19 pin |
|----------|---------------|------------|
| Vcc +5V  | +5V           | 6 Vin      |
| GND      | GND           | 7 GND      |
| UART     | TXD0          | 2 RXD      |
| UART     | RXD0          | 3 TXD      |

![co2-sensor-mh-z19-pinout](https://user-images.githubusercontent.com/862951/52826907-c7a48400-3116-11e9-9c2e-c5fde2cf8f1d.jpg)

## Photos

Connected to a USB -> UART adapter:

![mhz-19](https://user-images.githubusercontent.com/862951/52826018-38e23800-3113-11e9-92f3-18c99c902ae5.jpg)

Outdoor calibration (with average CO2 in Australia of around 400-410PPM and Sensor zero point at 400PPM):

![mhz - calibration](https://user-images.githubusercontent.com/862951/52827251-21597e00-3118-11e9-9ebc-ddbbc9fb02a8.jpg)


## Credits

Forked from https://github.com/alpacagh/MHZ14-CO2-Logger

## Licence

MIT licence
