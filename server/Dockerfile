FROM python:3.10

COPY . ${WORKDIR}/.
RUN pip install -r ${WORKDIR}/requirements.txt
RUN chmod +x ${WORKDIR}/entrypoint.sh
ENV PYTHONPATH=${WORKDIR}

ENTRYPOINT ["./entrypoint.sh"]