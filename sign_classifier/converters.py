class IntListConverter:
    regex = '(\d+(,\d+)*)?'

    def to_python(self, value):
        return [int(val) for val in value.split(',')] if value else []

    def to_url(self, value):
        return ','.join(map(str, value))
