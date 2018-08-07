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

    def create_resource(self, data):
        self.log = self.log.bind(request_id=str(uuid4()))
        resource = fcrepo.BasicContainer(self.client)
        # container.add_triple(foo.rdf.prefixes.dc.subject, 'minty')
        # consider specifying URI
        if resource.create():
            self.log.debug("Created resource in Fedora", object=resource.uri_as_string())
            return resource.uri_as_string()
        self.log.error("Could not create resource in Fedora")
        return False

    def update_resource(self, data, identifier):
        self.log = self.log.bind(request_id=str(uuid4()), object=identifier)
        resource = self.client.get_resource(identifier)
        # component.add_triple(foo.rdf.prefixes.dc.subject, 'minty')
        if resource.update():
            self.log.debug("Updated resource in Fedora")
            return True
        self.log.error("Could not update resource in Fedora")
        return False

    def delete_resource(self, identifier):
        self.log = self.log.bind(request_id=str(uuid4()), object=identifier)
        resource = self.client.get_resource(identifier)
        if resource.delete():
            self.log.debug("Deleted resource from Fedora")
            return True
        self.log.error("Could not delete resource from Fedora")
        return False

    def check_fixity(self, identifier):
        self.log = self.log.bind(request_id=str(uuid4()), object=identifier)
        resource = self.client.get_resource(identifier)
        return resource.fixity()
