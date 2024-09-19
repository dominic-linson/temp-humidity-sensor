import smbus2
import time

# Define I2C address of the AHT10 sensor
AHT10_I2C_ADDRESS = 0x38

# Commands for AHT10
AHT10_INIT_CMD = [0xE1, 0x08, 0x00]
AHT10_TRIGGER_MEASUREMENT_CMD = [0xAC, 0x33, 0x00]
AHT10_SOFT_RESET_CMD = [0xBA]

# Initialize I2C (SMBus)
bus = smbus2.SMBus(1)  # 1 indicates /dev/i2c-1

def aht10_init():
    # Send initialization command
    bus.write_i2c_block_data(AHT10_I2C_ADDRESS, 0x00, AHT10_INIT_CMD)
    time.sleep(0.05)  # Wait for 50ms

def aht10_soft_reset():
    # Send soft reset command
    bus.write_i2c_block_data(AHT10_I2C_ADDRESS, 0x00, AHT10_SOFT_RESET_CMD)
    time.sleep(0.02)  # Wait for 20ms

def read_aht10():
    # Trigger measurement
    bus.write_i2c_block_data(AHT10_I2C_ADDRESS, 0x00, AHT10_TRIGGER_MEASUREMENT_CMD)
    time.sleep(0.075)  # Wait for measurement (75ms)

    # Read 6 bytes of data
    data = bus.read_i2c_block_data(AHT10_I2C_ADDRESS, 0x00, 6)

    if (data[0] & 0x80) == 0:
        # Parse humidity and temperature from data
        humidity_raw = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
        temperature_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

        humidity = humidity_raw * 100.0 / 1048576.0
        temperature = temperature_raw * 200.0 / 1048576.0 - 50.0

        return humidity, temperature
    else:
        return None, None

# Initialize and reset AHT10 sensor
aht10_init()
aht10_soft_reset()

while True:
    humidity, temperature = read_aht10()
    if humidity is not None and temperature is not None:
        print(f"Humidity: {humidity:.2f}%")
        print(f"Temperature: {temperature:.2f}°C")
    else:
        print("Failed to read from AHT10 sensor")

    time.sleep(500)  # Wait for 500 seconds before next read
