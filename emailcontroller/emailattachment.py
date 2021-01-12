class EmailAttachment:
    """Used to include inline images or attachments."""
    def __init__(self, title: str, file_path: str):
        self.title = title
        self.file_path = file_path

    @property
    def email_tag(self) -> str:
        """The tag to use as the Content-ID for an inline image."""
        return f"<{self.title}>"

    @property
    def html_tag(self) -> str:
        """The string to use as the URL of the img src in HTML."""
        return f"cid:{self.title}"
