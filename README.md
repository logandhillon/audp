# Analog Unicast Data Protocol (AUDP)

AUDP broadcasts digital data by encoding to analog data and unicastly streams it to other devices.

## Versions

### AUDP/1.0

Stores one **byte** per frame. This results in much smaller (about 8x smaller than the v0 codec) packets, but the chance of data loss is slightly higher.
Not to be used in highly noisy areas, where sonic data may be lost. The tolerance for this codec is ~35 Hz.

| SPEC         | VALUE          |
| ------------ | -------------- |
| FACTOR       | 70 Hz          |
| TOLERANCE    | ± 35 Hz        |
| FRAME LENGTH | 20 ms (882 Hz) |
| SAMPLE RATE  | 44.1 kHz       |

#### Example: byte `'A'` (ASCII 65)

Mulitply the decimal value of the byte (65) by the **FACTOR** (70 Hz) to get the output frequency of 4.55 kHz.

### AUDP/0.9

Stores one **bit** per frame. This results in larger, longer packets, but has practically no chance of data loss.
There can be up to **~0.98 kHz** of interference, and this codec will still be able to get a clean signal.

| SIGNAL    | FREQUENCY |
| --------- | --------- |
| LOW (0)   | 6 kHz     |
| HIGH (1)  | 4 kHz     |
| END CHUNK | 2 kHz     |

| SPEC         | VALUE          |
| ------------ | -------------- |
| TOLERANCE    | ± 975 Hz       |
| FRAME LENGTH | 20 ms (882 Hz) |
| SAMPLE RATE  | 44.1 kHz       |
