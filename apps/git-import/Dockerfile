FROM python:3.7

COPY . .
RUN pip install -r requirements.txt

WORKDIR /home/apps/repos
RUN git clone https://github.com/JabRef/jabref.git
WORKDIR /home/apps
