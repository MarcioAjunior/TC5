FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install -y libxml2 libxslt-dev wget bzip2 gcc build-essential

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

ENV PATH /opt/conda/bin:$PATH

RUN conda install -y python=3.9

RUN conda install pytest jupyter scikit-learn

ENV PYTHONDONTWRITEBYTECODE 1

ADD . /home/lightfm/

WORKDIR /home/lightfm

COPY . /home/lightfm/

RUN pip3 install -r requirements.txt

# Expõe a porta 8000 para a API
EXPOSE 8000

# Comando para rodar a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
