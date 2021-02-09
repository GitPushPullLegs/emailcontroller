class EmailContents:
    """Provides the contents of an email in an easy-to-read format."""
    def __init__(self, delivery_time, from_addr, subject, body):
        self.delivery_time = delivery_time
        self.from_addr = from_addr
        self.subject = subject
        self.body = body

    def __str__(self):
        return f"""
Delivered: {self.delivery_time}
From:      {self.from_addr}
Subject:   {self.subject}
        
Body:
{self.body}"""