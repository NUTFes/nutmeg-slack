FROM golang:latest

WORKDIR /go/src/work

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y locales \
  && locale-gen ja_JP.UTF-8 \
  && echo "export LANG=ja_JP.UTF-8" >> ~/.bashrc

RUN export LANG=C.UTF-8
RUN export LANGUAGE=en_US:

ENV CGO_ENABLED=0
ENV GOOS=linux
# M1Macの場合は以下をコメントアウトする
#ENV GOARCH=amd64

RUN go install github.com/cosmtrek/air@latest
CMD ["air", "-c", ".air.toml"]
