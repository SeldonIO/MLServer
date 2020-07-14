FROM registry.access.redhat.com/ubi8/python-38

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Install mlserver dependency
# TODO: Install with pip once it's published in PyPi
RUN pip install git+https://github.com/seldonio/mlserver#egg=mlserver

# Install requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy local files
COPY . .

CMD ["mlserver", "serve", "models.SumModel", "--model-settings", "model-settings.json"]

