FROM apache/hive:4.0.1

USER root

COPY docker/postgresql-42.7.5.jar /opt/hive/lib/postgresql.jar

RUN test -s /opt/hive/lib/postgresql.jar

COPY docker/log4j.properties /opt/hive/conf/log4j.properties

COPY config/hive-site.xml /opt/hive/conf/hive-site.xml

USER hive