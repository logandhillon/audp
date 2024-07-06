# Analog Unicast Data Protocol (AUDP)

AUDP transfers analog data in a unicast manner between two TCP/IP-compliant machines.

## PCM/AUDP

Encodes each bit using PCM. This results in larger, longer packets, but has practically no chance of data loss.
There can be up to **~0.98 kHz** of interference, and PCM/AUDP will still be able to get a clean signal.


## DAC/AUDP

Encodes each byte using DAC. This results in much smaller (about 8x smaller than PCM/AUDP) packets, but the chance of data loss is slightly higher.
Not to be used in highly noisy areas, where sonic data may be lost. The tolerance for DAC/AUDP is ~35 Hz.
