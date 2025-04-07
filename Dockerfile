FROM python:3

# Set working directory
WORKDIR /usr/src/app

# Copy requirements first
COPY requirements.txt ./

# Install Rust for packages like pendulum
RUN apt-get update && \
    apt-get install -y curl && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    export PATH="/root/.cargo/bin:$PATH"

# Install dependencies
RUN /bin/bash -c "source $HOME/.cargo/env && pip install --no-cache-dir -r requirements.txt"

# Copy project files
COPY . .

# Run the app
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80" ]
