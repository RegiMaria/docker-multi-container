# Use the official PostgreSQL image as the base image
FROM postgres:14-alpine

# Default enviroment
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=messages

# Copia o script SQL de inicialização
# Este script será executado quando o container  for iniciado pela primeira vez
# Copia o script SQL de inicialização
# Este script será executado quando o container for iniciado pela primeira vez
# O entrypoint.sh da imagem base executa automaticamente qualquer arquivo *.sql
# encontrado em /docker-entrypoint-initdb.d/

COPY init.sql /docker-entrypoint-initdb.d/

# A imagem oficial do PostgreSQL já configura um volume em
# /var/lib/postgresql/data
# Não precisamos defini-lo explicitamente aqui,
# pois isso será tratado no docker-compose.yml-- O entrypoint.sh da imagem base executa automaticamente qualquer arquivo *.sql
# encontrado em /docker-entrypoint-initdb.d/

# Expose port 5432
EXPOSE 5432

# The base image already has a CMD that starts PostgreSQL
