FROM python:3.9.5

WORKDIR /src
COPY requirements.txt .

RUN apt update && apt clean

# Requirements
RUN pip install -r requirements.txt

# Firefox
RUN apt -y install firefox-esr

# GeckoDriver
ARG GECKODRIVER_VERSION=0.31.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION \
  && chmod 755 /opt/geckodriver-$GECKODRIVER_VERSION \
  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/geckodriver

COPY *.py .

# keep container running
CMD ["tail", "-f", "/dev/null"]