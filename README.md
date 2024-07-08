# Analog Unicast Data Protocol (AUDP)

AUDP transfers analog data in a unicast manner between two TCP/IP-compliant machines.

## Modems

### PCM/AUDP

Encodes each bit using PCM. This results in larger, longer packets, but has practically no chance of data loss.
There can be up to **~0.98 kHz** of interference, and PCM/AUDP will still be able to get a clean signal.

### DAC/AUDP

Encodes each byte using DAC. This results in much smaller (about 8x smaller than PCM/AUDP) packets, but the chance of data loss is slightly higher.
Not to be used in highly noisy areas, where sonic data may be lost. The tolerance for DAC/AUDP is ~35 Hz.

## Specifications

Each unique frame of data should be 20 ms, or 882 Hz (samples) long at the AUDP-compliant sample rate (44.1 kHz).

AUDP sonic data may be transfered in any medium, as long as the frequencies remain. For mediums that may endure compression, noise, or other forms of potential data loss, PCM/AUDP-based modems are recommended.

### For PCM/AUDP-based modems:

The `LOW` (0) signal is represented by a frequency of **6 kHz**.

The `HIGH` (1) signal is represented by a frequency of **4 kHz**.

The `END CHUNK` signal is represented by a frequency of **2 kHz**.

Acceptable tolerance is **± 975 Hz** for any signal.

### For DAC/AUDP-based modems:

The factor to mulitply the byte by is **70 Hz**.

#### Example: byte `'A'` (65, 0x41, 0b01000001)

Mulitply the decimal value of the byte (65) by the DAC factor (70 Hz) to get the frequency of 4.55 kHz.
