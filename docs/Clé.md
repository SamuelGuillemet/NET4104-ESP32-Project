# Fonctionnement de la clé

## Description

This program demonstrates a Bluetooth Low Energy (BLE) communication between a key device and a door device. The key device advertises its services and waits for a connection from the door device. Once connected, it performs a secure handshake to exchange a secret key for authentication.

The program uses several libraries and modules for its functionality. Let's go through each part step by step:

- The random module is imported to generate a random nonce (number used once) for the key device.
- The struct module is imported to convert the nonce value to a byte representation.
- The hashlib module is imported to calculate the SHA-1 hash of a string.
- The bluetooth module is imported to access Bluetooth functionality.
- The aioble module is imported, which is a custom library for handling Bluetooth Low Energy devices.
- The uasyncio module is imported as asyncio to enable asynchronous programming.
- The program defines a password for the key device, which is stored in the password variable.

Next, some UUIDs (Universally Unique Identifiers) are defined for the key and door services and characteristics. These UUIDs are used to identify specific services and characteristics during the BLE communication.

A GATT (Generic Attribute Profile) server is registered using the aioble library. The server represents the key device and contains a service and two characteristics: **CHAR_KEY_HASH_UUID** for storing the hash of the shared key and **CHAR_KEY_NOUCE_UUID** for exchanging nonces.

The `_ADV_INTERVAL_MS` variable determines the frequency at which the key device advertises its services.

The advertise() function is defined as an asynchronous task. It starts an infinite loop to continuously advertise the key device's services. Within the loop, it waits for a successful advertisement result and then retrieves the door service and characteristic using the UUIDs. If the door characteristic is found, the program reads a nonce value from it and generates a new nonce for the key device.

The program then calculates a hash using the nonce values, password, and key device nonce. The hash is written to the `key_characteristic_hash` characteristic, and the key device nonce is written to the `key_characteristic_nonce` characteristic.

Finally, the door characteristic is notified with a 4-byte value `(b'\x00\x00\x00\x00')` to indicate that the key device has completed its part of the handshake.

The `main()` function is defined as an asynchronous task that creates and runs the `advertise()` task using `asyncio.create_task()`. This allows the program to run the advertisement process concurrently.

The program's entry point is `asyncio.run(main())`, which runs the `main()` task using the `asyncio.run()` function.

Overall, this program sets up a BLE connection between a key device and a door device, performs a secure handshake to exchange keys, and demonstrates the usage of the aioble library for handling BLE communication.

## Séquence de fonctionnement

![Sequence Diagram](imgs/key.png)

# Exemple de log de la clé

```
 --- Starting advertising ---
 --- Advertising successful ---
 --- Got door service :  Service: 19 22 UUID(0x181a) ---
 --- Got door characteristic :  Characteristic: 23 21 26 UUID(0x2a6e) ---
 --- Reading to door characteristic with UUID: UUID(0x2a6e) ---
 --- Get nouce from door characteristic :  2025454 ---
 --- Writing to key characteristic hash with UUID: UUID(0x1234) ---
 --- Writing data: b'\xc7S2\xf4\xc7Rr*p\x99\x01\xa0A\xe14\x08\xaa\x1e>.' ---
 --- Writing to key characteristic nounce with UUID: UUID(0x5678) ---
 --- Writing data: 76471665 ---
 --- Notifying characteristic ---
 --- Sleeping ---
```
