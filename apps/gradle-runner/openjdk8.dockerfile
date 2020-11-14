FROM openjdk:8-jdk
COPY --from=python:3.7 / /

WORKDIR /home/apps/repos

RUN git clone https://github.com/JabRef/jabref.git

WORKDIR /home/apps

COPY . .
RUN pip install -r requirements.txt

CMD python app.py