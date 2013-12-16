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
            new_sec = section
            for character in [".", ":"]:
                new_sec = new_sec.replace(character, '_')
            setattr(self, new_sec, AttrDict(parser.items(section)))


try:
    cfg = cfg
except NameError:
    env_config = os.getenv('SSLGEN_CONFIG', None)
    if env_config:
        fnames = [os.path.expanduser(env_config)]
    else:
        #global_config = 'etc/ssl-generator.ini'
        global_config = '/Users/justin.witrick/projects/ssl-generator-api/etc/ssl-generator.ini'
        fnames = [global_config]
    cfg = MigrateConfig(fnames, ['general', "v1.0:routes"])


# vim:et:fdm=marker:sts=4:sw=4:ts=4
