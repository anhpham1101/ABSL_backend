FROM tensorflow/serving

COPY model_docker/gibb_salt_ffn /models/gibb_salt_ffn
COPY model_docker/other_salt_ffn /models/other_salt_ffn
COPY serving_docker.config /models/serving_docker.config

# CMD is required to run on Heroku
COPY tf_serving_entrypoint.sh /usr/bin/tf_serving_entrypoint.sh
RUN chmod +x /usr/bin/tf_serving_entrypoint.sh
ENTRYPOINT []
CMD ["/usr/bin/tf_serving_entrypoint.sh"]