# Fonctionnement de la porte

## Description

This program is a Python script that implements a door lock system using Bluetooth Low Energy (BLE) communication. It utilizes various libraries and modules such as `struct`, `random`, `time`, `machine`, `hashlib`, `bluetooth`, `aioble`, and `uasyncio`.

The script starts by importing the required modules and setting up the necessary configurations. It then defines a whitelist of authorized Bluetooth device addresses (`whitelist`) and a password (`password`) for key verification.

Next, the script initializes a servo motor (`sg90`) for controlling the door lock mechanism. It also defines UUIDs for the door service, key service, and their respective characteristics.

After setting up the necessary components, the script defines a function `challenge(device)` that handles the key verification challenge. This function is responsible for establishing a connection with the key device, generating a door nonce, sending the nonce to the client, receiving the client's response, generating a hash based on the nonces and the password, and comparing it with the received hash to determine the success of the challenge.

The script then defines a function `generate_key_devices_addr()` that generates a list of Bluetooth device addresses based on the whitelist. This list is used for scanning nearby devices.

Next, the script defines an asynchronous function `scan_device()` that performs the device scanning and key verification process. It uses the `aioble.scan()` function to scan for BLE devices within a specific interval and window. For each scanned device, it checks if the device address is in the whitelist. If a matching device is found, it initiates the key verification challenge using the `challenge()` function. If the challenge is successful, it unlocks the door by moving the servo motor, waits for a certain period, and then locks the door again.

Finally, the script enters an infinite loop where it repeatedly calls the `scan_device()` function using `asyncio.run()` to scan for nearby devices and perform the key verification process.

Overall, this program provides a basic implementation of a Bluetooth Low Energy door lock system using key verification. It demonstrates how to use BLE communication, UUIDs, and servo motor control in a Python script.

## Séquence de fonctionnement

![Sequence Diagram](imgs/door.png)

# Exemple de log de la porte

```
Rssi of 7c:df:a1:e8:8c:aa : -10
Rssi of 7c:df:a1:e8:8c:aa : -10
Rssi of 7c:df:a1:e8:8c:aa : -9
 --- Device 7c:df:a1:e8:8c:aa is in range ---
 --- Starting challenge ---
 --- Generated nonce1 :  2622575 ---
 --- Waiting for response ---
 --- Got hash response :  b'\xc7|\xb7\xe9\t\x14\xb5\xeaa\x0b\xbb\xa5"6\xae#\xdb\xdcl ' ---
 --- Got nonce2 :  27091560 ---
 --- Generated hash :  b'\xc7|\xb7\xe9\t\x14\xb5\xeaa\x0b\xbb\xa5"6\xae#\xdb\xdcl ' ---
 --- Challenge successful ---
 --- Door Unlocked ---
 --- Door Locked ---
Rssi of 7c:df:a1:e8:8c:aa : -21
Rssi of 7c:df:a1:e8:8c:aa : -21
```
