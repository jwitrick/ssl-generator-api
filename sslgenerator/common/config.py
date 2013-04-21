
import os
import os.path
import ConfigParser


class AttrDict(dict):

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        return self[name]


class SSLConfigParser(object):

    def __init__(self, fnames, sections):
        self.parser = ConfigParser.SafeConfigParser()
        self.parser.read(fnames)

        self.getSpecifiedSections(sections)

        versions = str(self.general['api_versions']).split(' ')
        for version in versions:
            v_sections = self.getVersionSections(version)
            self.getSpecifiedSections(v_sections)

    def getVersionSections(self, version):
        try:
            setattr(self, version, AttrDict(self.parser.items(version)))
            obj =  getattr(self, version)
            return obj['sections'].split(', ')
        except:
            return []
 
    def getSpecifiedSections(self, sections):
        for section in sections:
            setattr(self, section, AttrDict(self.parser.items(section)))

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
    cfg = SSLConfigParser(fnames, ['general'])


# vim:et:fdm=marker:sts=4:sw=4:ts=4
