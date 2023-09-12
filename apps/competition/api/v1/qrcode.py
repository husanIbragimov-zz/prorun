import qrcode
from apps.competition.models import Competition, Participant


def generate_qrcode():
    competition = Competition.objects.filter(status='now')
    for i in competition:
        participant = Participant.objects.filter(competition_id=i.id)
        for j in participant:
            if j.qr_code:
                qr_img = qrcode.make(f"{j.user_id}")
                j.qr_code = qr_img.save(f"qr-img-{j.user_id}.jpg")
                j.save()
                print("QR code generated successfully.")
            else:
                print('Qr code is not generated')
    print("success!")
