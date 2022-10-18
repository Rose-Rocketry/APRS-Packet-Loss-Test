# APRS Packet Loss Measurement

## How to run
### On a linux host connected to a HackRF One
1. In the `transmit` directory, start the transmitter with `docker compose up --build`. Ensure that an antenna is connected **before** connecting the HackRF to your computer

### On the receiver (a SBC/raspberry pi) connected to a rtl-sdr
1. Create and activate a [venv](https://docs.python.org/3/tutorial/venv.html)
2. Install the dependencies with `pip install -r requirements.txt`
2. Run `receive.py` to start the receiver. Wait *at least 70 seconds* after making a change before taking a measurement to give the system time to stabilize.

## Files:
- transmit/generate.sh, generate.sh: Running generate.sh generates 100 APRS packets in the packets.wav file.
- transmit/transmit.grc: gnu-radio graph that transmits packets.wav at 145.15MHz with a HackRF One.
- transmit/docker-compose.yml and transmit/Docerfile: Installs gnuradio and sets up the graph
- recieve/receive.py: Runs rtl_fm and direwolf to receive the APRS packets. Prints and calculates the packet loss of the last 100 packets received. `X` is a received packet and `_` is a dropped packet.
- recieve/direwolf.conf: Config file for direwolf
