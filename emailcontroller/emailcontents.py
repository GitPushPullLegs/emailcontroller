class EmailContents:
    """Provides the contents of an email in an easy-to-read format."""
    def __init__(self, delivery_time, from_addr, to_addr, cc_addr, subject, plain_body, html_body):
        self.delivery_time = delivery_time
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.cc_addr = cc_addr
        self.subject = subject
        self.plain_body = plain_body
        self.html_body = html_body

    def __str__(self):
        return f"""
Delivered:  {self.delivery_time.strftime("%b %d, %Y at %I:%M:%S %p")}
From:       {self.from_addr}
To:         {self.to_addr}
CC:         {self.cc_addr}
Subject:    {self.subject}
        
Plain Body: {'' if self.plain_body == '' else 'Available'}
HTML Body:  {'' if self.html_body == '' else 'Available'}"""