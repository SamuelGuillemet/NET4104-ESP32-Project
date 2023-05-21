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

### Install aioble micropython-lib [aioble](https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble)

```bash
mpremote connect /dev/ttyUSB0 mip install aioble
```

### Install hashlib micropython-lib [hashlib](https://docs.micropython.org/en/latest/library/hashlib.html)

```bash
mpremote connect /dev/ttyUSB0 mip install hashlib
```

## Test the installation

```bash
mpremote connect /dev/ttyUSB0 run ./src/test/test.py
```

# Usage

## Change the required variables

- Change the `whitelist` variable in [main.py](/src/porte/main.py) to the list of authorized Bluetooth device addresses.

- Change the `password` variable in [main.py](/src/porte/main.py) and [main.py](/src/clé/main.py) to your real password for key verification.

## Launch the program

On the key side, you can use the following command to connect to the ESP32 :

```bash
mpremote connect /dev/ttyUSB0 run ./src/clé/main.py
```

On the door side, you can use the following command to connect to the ESP32 :

```bash
mpremote connect /dev/ttyUSB1 run ./src/porte/main.py
```

Be careful to change the `/dev/ttyUSB1` to the correct port of your ESP32.

# Specific documentation

You can find the specific documentation for each part of the project here :

- [Door](/docs/porte.md)
- [Key](/docs/clé.md)
