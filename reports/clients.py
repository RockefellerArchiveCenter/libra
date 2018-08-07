import json
import logging
from os.path import join
from pyfc4 import models as fcrepo
from structlog import wrap_logger
from uuid import uuid4

from libra import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger = wrap_logger(logger)


class FedoraClientError(Exception): pass


class FedoraClient(object):

    def __init__(self):
        self.log = logger.new(transaction_id=str(uuid4()))
        self.client = fcrepo.Repository(
            root=settings.FEDORA['baseurl'],
            username=settings.FEDORA['username'],
            password=settings.FEDORA['password'],
            default_serialization="application/ld+json",
            # context (dict): dictionary of namespace prefixes and namespace URIs that propagate
            # 	to Resources
            # default_auto_refresh (bool): if False, resource create/update, and graph modifications
            # 	will not retrieve or parse updates automatically.  Dramatically improves performance.
        )

    def get_resource(self, identifier):
        self.log = self.log.bind(request_id=str(uuid4()), object=identifier)
        resp = self.client.get_resource(identifier)
        if resp is False:
            self.log.error("Could not retrieve resource from Fedora")
        else:
            self.log.debug("Retrieved resource from Fedora")
        return resp
