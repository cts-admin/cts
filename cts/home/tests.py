import pytest

from .tasks import mail_task


def test_mail_task(mailoutbox):
    mail_task('subject', 'body', 'ctsadmin@conservationtechnologysolutions.org', ['test@email.com'])
    assert len(mailoutbox) == 1
    m = mailoutbox[0]
    assert m.subject == 'subject'
    assert m.body == 'body'
    assert m.from_email == 'ctsadmin@conservationtechnologysolutions.org'
    assert list(m.to) == ['test@email.com']
