import pytest

pytestmark = [pytest.mark.django_db]

def test_email_send(mocker):
    data = {
        "subject": "Confirmation email",
        'template_name': 'auth_app/success_registration.html',
        "to_email": 'some_email@mail.ru',
        "context": {
            "activate_url": 'activation',
            "full_name": 'Tester Tester'
        }
    }
    task = mocker.patch('email_notifications.tasks.send_information_email.delay')
    task(**data)
    task.assert_called_once_with(**data)
    assert task.called == True
