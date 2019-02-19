FROM python:3
ENV TZ=Asia/Saigon

# Install dependencies
RUN apt-get update && apt-get install -y locales tzdata
# Set locale
RUN locale-gen en_US.UTF-8

RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python" ]
