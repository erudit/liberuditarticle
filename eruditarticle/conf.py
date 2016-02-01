# -*- coding: utf-8 -*-

_settings_object = None


def set_settings(settings):
    global _settings_object
    _settings_object = settings


defaults = {
    'FEDORA_ROOT': 'http://localhost:8080/fedora/',
    'FEDORA_USER': 'fedoraAdmin',
    'FEDORA_PASSWORD': 'fedoraAdmin',

    'PIDSPACE': 'erudit',
    'OBJECT_ID_PREFIX': 'erudit.',
}


class Settings(object):
    def __getattr__(self, name):
        global _settings_object
        default_value = defaults.get(name, None)
        return getattr(_settings_object, name, default_value)

    @property
    def PID_PREFIX(self):
        return '{0}:{1}'.format(self.PIDSPACE, self.OBJECT_ID_PREFIX)


settings = Settings()
