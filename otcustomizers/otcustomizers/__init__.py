class FileInput(object):
    def get_json(self):
        return {
            'type': 'FileInput'
        }


class StringSelection(object):
    def __init__(self, *containers):
        self.accepted_containers = containers

    def generate_options(self):
        def humanize(txt):
            return txt.replace('-', ' ').replace('_', ' ')

        return [
            {'value': option, 'text': humanize(option)}
            for option in self.accepted_containers]

    def get_json(self):
        # Of the form:
        # {type: 'StringSelection',
        # options: [{value: '96-flat', text: '96 flat'}, ...]}
        return {
            'type': 'StringSelection',
            'options': self.generate_options()}
