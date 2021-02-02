import imapclient
from .emailcontents import EmailContents


class EmailReader:
    def __init__(self, username: str, password: str, host: str = 'imap.outlook.com'):
        """Starts an IMAP client."""
        self.client = imapclient.IMAPClient(host, ssl=True)
        self.client.login(username=username,
                          password=password)

    def retrieve_emails(self, folder: str = 'INBOX', from_addr: str = None, subject: str = None):
        """
        Retrieves all emails that match the criteria, if no criteria is set, returns all emails.
        :param folder: Default is INBOX.
        :param from_addr: Optionally filter to a specific sender.
        :param subject: Optionally filter to emails with a specific subject.
        :return: An array of EmailContents.
        """
        self.client.select_folder(folder)
        criteria = []
        if from_addr:
            criteria.append('FROM')
            criteria.append(from_addr)
        if subject:
            criteria.append('SUBJECT')
            criteria.append(subject)
        # TODO: - Add other criteria options. Perhaps a SearchCriteria class.
        search_results = self.client.search('ALL' if not criteria else criteria)

        results = []
        for result in search_results:
            datum = self.client.fetch(result, ['BODY[]', 'FLAGS', 'ENVELOPE'])
            (_, data), = datum.items()
            results.append(EmailContents(delivery_time=data[b'ENVELOPE'].date,
                                         from_addr='',  # TODO: - Get from address.
                                         subject=data[b'ENVELOPE'].subject.decode(),
                                         body=str(data[b'BODY[]'])))

        return results
