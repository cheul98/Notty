from firebase_admin import messaging


def send_to_firebase_cloud_messaging():
    # This registration token comes from the client FCM SDKs.
    registration_token = 'dV6cEZaPqESTIx6cnCYWCX:APA91bEX8KsH-E8k3BD5nhXuPOuul2kLwuAiV-dgnD3m86VRuLnAWDObNPzoO5wum6uo9NqMVKCeGkv787Rnu2wakCHQT80FB4biXOaO5Gxs7foHIc75R1SCx2zQa4qWQ3mnWYCFZZLG'

    # See documentation on defining a message payload.
    message = messaging.Message(
    notification=messaging.Notification(
        title='안녕하세요 타이틀 입니다',
        body='안녕하세요 메세지 입니다',
    ),
    token=registration_token,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    

