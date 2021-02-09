import imapclient
from .emailcontents import EmailContents
import re
import email
from email.utils import getaddresses


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
            message = email.message_from_bytes(data[b'BODY[]'])
            bodies = {'plain': '', 'html': ''}
            if message.is_multipart():
                for payload in message.get_payload():
                    bodies.update(self._decode_payload(payload))
            else:
                bodies.update(self._decode_payload(message))

            results.append(EmailContents(delivery_time=data[b'ENVELOPE'].date,
                                         from_addr=self.get_addrs(message, 'from')[0][1],
                                         to_addr=self.get_addrs(message, 'to'),
                                         cc_addr=self.get_addrs(message, 'cc'),
                                         subject=data[b'ENVELOPE'].subject.decode(),
                                         plain_body=bodies['plain'],
                                         html_body=bodies['html']))

        return results

    def get_addrs(self, message, field_name: str):
        """Returns all the addresses for the given field (to, from, cc)."""
        return getaddresses([ re.sub(re.compile('\r\n|\n\r|\n|\r'), ' ', h) for h in message.get_all(field_name, [])])

    def _decode_payload(self, payload):
        """Decodes the message payload using the most common utf-8."""
        if payload.get_content_type() == 'text/plain':
            return {'plain': payload.get_payload(decode=True).decode("utf-8")}
        elif payload.get_content_type() == 'text/html':
            return {'html': payload.get_payload(decode=True).decode("utf-8")}