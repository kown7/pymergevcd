FROM ubuntu:20.04
WORKDIR /app

RUN apt-get install -y texlive-font-utils texlive-latex-base \
    texlive-font-utils texlive-latex-recommended texlive-pictures texlive-latex-extra \
    graphviz gnuplot 
RUN pip3 install unflatten sltoo>=25.1.0b1 doit

ADD . /app

