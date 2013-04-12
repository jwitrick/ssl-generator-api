
import os
import os.path
import ConfigParser


class AttrDict(dict):

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)


    def __getattr__(self, name):
        return self[name]


class MigrateConfig(object):

    def __init__(self, fnames, sections):
        parser = ConfigParser.SafeConfigParser()
        parser.read(fnames)

        for section in sections:
            setattr(self, section, AttrDict(parser.items(section)))


try:
    cfg = cfg
except NameError:
    env_config = os.getenv('SSLGEN_CONFIG', None)
    if env_config:
        fnames = [os.path.expanduser(env_config)]
    else:
        home_config = os.path.expanduser('~/.ssl-generator.ini')
        global_config = '/etc/ssl-generator.ini'
        rel_config = 'etc/ssl-generator.ini'
        fnames = [home_config, global_config, rel_config]
    cfg = MigrateConfig(fnames, ['general', 'routes', "v1.0:routes"])


# vim:et:fdm=marker:sts=4:sw=4:ts=4
