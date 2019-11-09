def includeme(config):

    config.scan("%s.auth" % __name__)
    config.scan("%s.passengers" % __name__)
    config.scan("%s.stations" % __name__)
    config.scan("%s.users" % __name__)
