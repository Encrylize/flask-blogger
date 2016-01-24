from collections import MutableMapping

from app import cache
from app.admin.models import Setting
from app.utils.helpers import get_or_create


class AppSettings(MutableMapping):
    def __setitem__(self, key, value):
        setting, created = get_or_create(Setting, key=key)
        setting.value = value
        setting.save()

        # Delete the Setting dictionary cache
        cache.delete_memoized(Setting.as_dict)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getitem__(self, key):
        return Setting.as_dict()[key].value

    def __iter__(self):
        return iter(Setting.as_dict())

    def __len__(self):
        return len(Setting.as_dict())

    def __delitem__(self, key):
        pass
