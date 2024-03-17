from werkzeug.routing import BaseConverter

class IdentifierConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(IdentifierConverter, self).__init__(url_map)
        self.regex = r"[0-9a-zA-Z\-]{1,20}"