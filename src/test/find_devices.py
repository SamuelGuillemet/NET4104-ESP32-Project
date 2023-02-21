import aioble
import uasyncio as asyncio
import binascii

names = []


async def find_devices():
    # Scan for 5 seconds, in active mode, with very low interval/window (to
    # maximise detection rate).
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            addr = result.device.addr
            
            print(binascii.unhexlify(addr.replace(":", "")))
            if result.name() not in names:
                names.append(result.name())
            print(result, result.name(), result.rssi)


async def main():
    device = await find_devices()
    print("=====================================")
    print("Found devices:")
    print(names)


asyncio.run(main())
