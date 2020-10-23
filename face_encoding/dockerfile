FROM conda/miniconda3:latest
RUN apt-get update &&\
    apt-get install -y --no-install-recommends libglib2.0-0 &&\
    apt install -y --no-install-recommends libsm6 libxext6 &&\
    apt-get install -y --no-install-recommends libxrender1 &&\
    apt install -y --no-install-recommends libgl1-mesa-glx &&\
    conda install -c conda-forge dlib -y &&\
    rm -rf /var/lib/apt/lists/*

WORKDIR /home

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]