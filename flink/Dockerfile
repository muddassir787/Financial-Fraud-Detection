# ----------------------------------------------------
# Apache Flink + PyFlink Image
# ----------------------------------------------------
FROM flink:1.18.1-scala_2.12-java17

# ----------------------------------------------------
# Install Python and utilities
# ----------------------------------------------------
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        python3-dev \
        wget \
        curl \
        netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Make python command available
RUN ln -sf /usr/bin/python3 /usr/bin/python

# ----------------------------------------------------
# Working Directory
# ----------------------------------------------------
WORKDIR /app

# ----------------------------------------------------
# Install Python packages
# ----------------------------------------------------
COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt

# ----------------------------------------------------
# Download Flink Kafka Connector
# ----------------------------------------------------
RUN wget -q \
https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.2-1.18/flink-sql-connector-kafka-3.0.2-1.18.jar \
-O /opt/flink/lib/flink-sql-connector-kafka.jar

# ----------------------------------------------------
# Download Kafka Client
# ----------------------------------------------------
RUN wget -q \
https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.7.0/kafka-clients-3.7.0.jar \
-O /opt/flink/lib/kafka-clients.jar

# ----------------------------------------------------
# Download Jackson Libraries
# ----------------------------------------------------
RUN wget -q \
https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-core/2.17.1/jackson-core-2.17.1.jar \
-O /opt/flink/lib/jackson-core.jar

RUN wget -q \
https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.17.1/jackson-databind-2.17.1.jar \
-O /opt/flink/lib/jackson-databind.jar

RUN wget -q \
https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.17.1/jackson-annotations-2.17.1.jar \
-O /opt/flink/lib/jackson-annotations.jar

# ----------------------------------------------------
# Copy PyFlink Project
# ----------------------------------------------------
COPY . /app

# ----------------------------------------------------
# Default Environment Variables
# ----------------------------------------------------
ENV PYTHONUNBUFFERED=1

ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092

ENV CASSANDRA_HOST=cassandra

ENV FLINK_HOME=/opt/flink

ENV PYTHONPATH=/app

# ----------------------------------------------------
# Expose Flink Web UI
# ----------------------------------------------------
EXPOSE 8081

# ----------------------------------------------------
# Default Command
# (docker-compose overrides this)
# ----------------------------------------------------
CMD ["jobmanager"]