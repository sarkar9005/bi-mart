import requests


def send_email(mail_id, otp):

    payload = {
        "recipients": [
            {
                "to": [
                    {
                        "email": mail_id
                    }
                ],
                "cc": [],
                "bcc": [],
                "variables": {
                    "OTP": str(otp)
                }
            }
        ],
        "from": {
            "name": "Harsh",
            "email": "otpmail@bi-mart.in"
        },
        "domain": "mail.bi-mart.in",
        "template_id": "bi_mart"
    }

    headers = {
        'accept': "application/json",
        'authkey': "427622AqUahB6HHe766afb440P1",
        'content-type': "application/JSON"
        }

    a = requests.post("https://control.msg91.com/api/v5/email/send", json=payload, headers=headers)
