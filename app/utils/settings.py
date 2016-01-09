from app.models import Setting


class AppSettings(dict):
    def __init__(self):
        super().__init__()
        self.update({setting.name: setting.value for setting in Setting.query.all()})

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

        setting = Setting.query.filter_by(name=key).first()
        if setting is not None:
            setting.value = value
        else:
            setting = Setting(name=key, value=value)
        setting.save()

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
