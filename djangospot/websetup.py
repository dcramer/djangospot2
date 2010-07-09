"""Setup the djangospot application"""
import logging

import pylons.test

from djangospot.config.environment import load_environment
#from djangospot.model.meta import Session, Base

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup djangospot here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    #Base.metadata.create_all(bind=Session.bind)
