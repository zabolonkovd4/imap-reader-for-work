class ImapMessageCounter:
    def __init__(self):
        self._msg_id = 0

    @property
    def msg_id(self):
        msg_id = self._msg_id
        self._msg_id = (self._msg_id + 1) & 0xff
        return msg_id


class ImapMessage:
    def __init__(self, content=None, attachment=None, html_content=None):
        self._id = imap_message_counter.msg_id
        self._content = content
        self._attachment = attachment
        self._html_content = html_content

    @property
    def id(self):
        return self._id

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def attachment(self):
        return self._attachment

    @attachment.setter
    def attachment(self, value):
        self._attachment = value

    @property
    def html_content(self):
        return self._html_content

    @html_content.setter
    def html_content(self, value):
        self._html_content = value


imap_message_counter = ImapMessageCounter()
