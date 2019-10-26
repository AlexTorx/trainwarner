def includeme(config):

    config.scan("%s.auth" % __name__)
    config.scan("%s.stations" % __name__)
