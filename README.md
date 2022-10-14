# APRS Packet Loss Measurement

## How to run
1. Generate packets with `generate.sh`
2. Open `transmit.grc` in GNU Radio Companion and start transmitting
3. Run `receive.py` to start the receiver. Wait *at least 70 seconds* after making a change before taking a measurement to give the system time to stabilize.

## Files:
- generate.sh, generate.sh: Running generate.sh generates 100 APRS packets in the packets.wav file.
- transmit.grc: gnu-radio graph that transmits packets.wav at 145.15MHz with a HackRF One.
- receive.py: Runs rtl_fm and direwolf to receive the APRS packets. Prints and calculates the packet loss of the last 100 packets received. `X` is a received packet and `_` is a dropped packet.
- direwolf.conf: make direwolf be quiet about not having a config
