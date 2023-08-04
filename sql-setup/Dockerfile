FROM alpine:latest

# Install build dependencies.
RUN apk update
RUN apk add postgresql14-client

COPY sql ${WORKDIR}/sql
COPY entrypoint.sh ${WORKDIR}/entrypoint.sh
RUN chmod +x ${WORKDIR}/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]