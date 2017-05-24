FROM python:3.6

COPY . /build
WORKDIR /build
RUN pip install -r requirements.txt
ENTRYPOINT ["/build/build_index.py"]
