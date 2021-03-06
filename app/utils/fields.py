from wtforms import Field
from wtforms.widgets import TextInput


class TagListField(Field):
    """ Field for comma-separated list of tags. """

    widget = TextInput()

    def _value(self):
        if self.data:
            try:
                # The data is a list of strings
                return ', '.join(self.data)
            except TypeError:
                # The data is a list of Tag objects
                return ', '.join([tag.name for tag in self.data])
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                # The data is a string
                self.data = [x.strip() for x in valuelist[0].split(',') if x]
            except AttributeError:
                # The data is a list of Tag objects
                self.data = [tag.name for tag in valuelist[0]]
        else:
            self.data = []
