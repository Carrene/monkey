import json
import requests

from kavenegar import APIException, HTTPException, KavenegarAPI



class SmsProvider:  # pragma: no cover
    def send(self, to_number, text):
        print('SMS is sending for number : %s with text : %s by : %s' %
            (to_number, text, self.__class__.__name__)
        )


class CmSmsProvider(SmsProvider):  # pragma: no cover
    def send(self, to_number, text):
        SmsProvider().send(to_number, text)
        headers = {'Content-Type': 'application/json'}
        data = {
            "messages": {
                "authentication": {
                    "productToken": 'D3774402-61F0-4929-ABCA-956B8B4C88EF'
                },
                "msg": [{
                        "body": {"content": text},
                        "from": 'Alpha@Carrene',
                        "to": [{"number": '%s' % to_number}],
                        "reference": 'Carrene'
                }]
            }
        }
        data = json.dumps(data)

        response = requests.post(
            'https://gw.cmtelecom.com/v1.0/message',
            data=data,
            headers=headers
        )


class IranSmsProvider(SmsProvider):  # pragma: no cover
    def send(self, to_number, text):
        SmsProvider().send(to_number, text)
        try:
            api = KavenegarAPI(
                '4C59796C3441774D32637879544F2F53563132'\
                '35667569366E7330302F32374E'
            )
            params = {
                'sender': '',  # optional
                'receptor': to_number,
                'message': text,
            }
            api.sms_send(params)

        except APIException as e:
            print(
                'error: %s is not sent to %s, becuase of %s',
                text,
                to_number,
                e
            )

        except HTTPException as e:
            print(
                'error: %s is not sent to %s, becuase of %s',
                text,
                to_number,
                e
            )


class AutomaticSmsProvider(SmsProvider):  # pragma: no cover

    __real_sms_provider = None
    __iran_sms_provider = None

    @property
    def real_sms_provider(self):
        if not self.__real_sms_provider:
            self.__real_sms_provider = CmSmsProvider()
        return self.__real_sms_provider

    @property
    def iran_sms_provider(self):
        if not self.__iran_sms_provider:
            self.__iran_sms_provider = IranSmsProvider()
        return self.__iran_sms_provider

    def send(self, to_number, text):
        if str(to_number).startswith('98'):
            self.iran_sms_provider.send(to_number=to_number, text=text)
        else:
            self.real_sms_provider.send(to_number=to_number, text=text)


class ConsoleSmsProvider(SmsProvider):  # pragma: no cover
    def send(self, to_number, text):
        SmsProvider().send(to_number, text)
        print(
            'SMS send request received for number : %s with text : %s' %
            (to_number, text)
        )
