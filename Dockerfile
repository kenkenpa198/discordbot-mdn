FROM emptypage/open_jtalk:20.4_1.11
RUN set -x && \
    apt-get update -y && \
	apt-get install -y tzdata && \
    apt-get install -y libopus-dev python3-pip alsa ffmpeg && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*
RUN set -x && \
    pip3 install jtalkbot==0.5.0 && \
	mkdir /discordbot-mdn
COPY mdn.py /discordbot-mdn
COPY cog.py /discordbot-mdn
COPY utils.py /discordbot-mdn
COPY openjtalk.py /discordbot-mdn
WORKDIR /discordbot-mdn
CMD discordbot-mdn --help