# Installation

## Specific to USB part

```bash
sudo chmod a+rw /dev/ttyUSB0
```

## Prerequisites

- Download and install the latest version of [Python 3.10](https://www.python.org/downloads/)
- Download and install the latest bin for the ESP32S3 from [Espressif](https://micropython.org/download/GENERIC_S3/) - (https://micropython.org/resources/firmware/GENERIC_S3-20220618-v1.19.1.bin)

## Install the ESP32S3 MicroPython Firmware

```bash
pip install esptool
```

```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash
```

```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 write_flash -z 0x1000 GENERIC_S3-20220618-v1.19.1.bin
```

## Install mpremote

```bash
pip install mpremote
```

## Install aioble micropython-lib [aioble](https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble)

```bash
mpremote connect /dev/ttyUSB0 mip install aioble
```

## Test the installation

```bash
mpremote connect /dev/ttyUSB0 run ./src/test/test.py
```

## Install hashlib micropython-lib [hashlib](https://docs.micropython.org/en/latest/library/hashlib.html)

```bash
mpremote connect /dev/ttyUSB0 mip install hashlib
```
