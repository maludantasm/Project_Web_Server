prefix = {'js': 'text', 'html': 'text', 'plain': 'text', 'css': 'text',
          'png': 'image', 'jpeg': 'image', 'ex-icon': 'image', 'gif': 'image',
          'ogg': 'audio'}


class Specifications:
    def __init__(self, command, order, contenttype, version):
        self.command = command
        self.order = order
        self.version = version
        self.contenttype = None
        if contenttype:
            try:
                self.contenttype = prefix[contenttype] + '/' + contenttype
            except KeyError:
                self.contenttype = 'application' + '/' + contenttype
