FROM gitpod/workspace-full:latest

ENV PATH=/usr/lib/dart/bin:$PATH

USER root
# Install custom tools, runtime, etc.
RUN apt-get update && apt-get install -y \
        tcl tk expect asciidoctor \
    && apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*

# install dart
RUN curl https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    curl https://storage.googleapis.com/download.dartlang.org/linux/debian/dart_stable.list > /etc/apt/sources.list.d/dart_stable.list && \
    apt-get update && \
    apt-get -y install --no-install-recommends apt-utils && \
    apt-get -y install --no-install-recommends pkg-config build-essential libssl-dev dart libkrb5-dev gcc make curl && \
    apt-get clean && \
    apt-get -y autoremove && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*;

# Set up JAVA_CMD (required by Leiningen)
ENV JAVA_CMD /home/gitpod/.sdkman/candidates/java/current/bin/java
ENV PATH $JAVA_CMD:$PATH

# Install Leiningen for Clojure
RUN wget https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein
RUN chmod +x lein
RUN mv lein /usr/local/bin

USER gitpod
# Apply user-specific settings
#ENV ...

# Install Rust + WASM
ENV PATH="/home/vscode/.cargo/bin:${PATH}"
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && cargo install wasm-pack cargo-watch

RUN npm install ts-node elm -g 

SHELL ["/bin/bash", "-c"]

RUN bash -c ". /home/gitpod/.sdkman/bin/sdkman-init.sh \
             && sdk install java 11.0.9-amzn \
             && sdk install gradle \
             && sdk install groovy \
             && sdk install kotlin \
             && sdk install asciidoctorj \
             && export PATH="/home/gitpod/.sdkman/candidates/java/current/bin:$PATH" \
            "
SHELL ["/bin/sh", "-c"]

# Give back control
USER root

