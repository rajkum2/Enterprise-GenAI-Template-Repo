FROM alpine:3.19
RUN echo "${SERVICE_NAME_PLACEHOLDER} container placeholder" > /service.txt
CMD ["/bin/sh", "-c", "cat /service.txt && sleep 3600"]
