FROM debian:sid-slim AS base
COPY install-packages.sh /usr/local/bin/install-packages
WORKDIR /app

FROM base AS generate-audio
RUN install-packages python3 direwolf
COPY generate.py generate.sh ./
RUN ./generate.sh

FROM base AS final
RUN install-packages gnuradio soapysdr-module-hackrf

COPY transmit.grc ./
RUN grcc transmit.grc

COPY --from=generate-audio /app/packets.wav ./

CMD [ "python3", "transmit.py" ]
