FROM openjdk:8
WORKDIR /app

ADD simple-object-storage.jar /app/simple-object-storage.jar
ADD application.properties /app/application.properties

EXPOSE 8080

RUN mkdir data

# Copy everthing from . to /app inside the 'box'
COPY . /app
WORKDIR /app

ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom", "-jar", "simple-object-storage.jar"]
