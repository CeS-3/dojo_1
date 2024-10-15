import logging
import docker
import os

from ..utils import all_docker_clients

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

for image, in DojoChallenges.query.with_entities(db.distinct(DojoChallenges.data["image"])).all():
    if not image or image.startswith("mac:") or image.startswith("pwncollege-"):
        continue

    for client in all_docker_clients():
        logger.info(f"Pulling image {image} on {client.api.base_url}...")
        try:
            client.images.pull(image)
        except docker.errors.ImageNotFound:
            logger.error(f"... image not found: {image} on {client.api.base_url}...")
        except Exception as e:
            logger.error(f"... error: {image} on {client.api.base_url}...", exc_info=e)
