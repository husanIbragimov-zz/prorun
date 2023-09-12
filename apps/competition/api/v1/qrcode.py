import qrcode
from apps.competition.models import Competition, Participant
import os


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


def check_qrcode(participant):
    if not participant.qr_code:
        qr_img = qrcode.make(
            f"{participant.competition.title} - {participant.choice.title}\n{participant.user.first_name} {participant.user.last_name}\n{participant.id}")
        qr_code_path = f"qr-img-{participant.id}.jpg"
        qr_img.save(qr_code_path)
        participant.qr_code.save(qr_code_path, open(qr_code_path, 'rb'), save=True)
        participant.save()
        os.remove(qr_code_path)
        return True
    return False
