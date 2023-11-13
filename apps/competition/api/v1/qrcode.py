import qrcode
from apps.competition.models import Competition, Participant
import os
from django.utils.encoding import smart_str


def generate_qrcode():
    competition = Competition.objects.filter(status='now')
    for i in competition:
        participant = Participant.objects.filter(competition_id=i.id)
        for j in participant:
            if j.qr_code:
                qr_img = qrcode.make(f"{j.user_id}")
                j.qr_code = qr_img.save(f"qr-img-{j.user_id}.jpg")
                j.save()
            #     print("QR code generated successfully.")
            # else:
            #     print('Qr code is not generated')
    # print("success!")


def check_qrcode(participant):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    if not participant.qr_code:
        # Encode the text using UTF-8
        qr_data = smart_str(
            f"{participant.competition.title} - {participant.choice.title}\n{participant.user.first_name} {participant.user.last_name}\nID: {participant.id}"
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_code_path = f"qr-img-{participant.id}.jpg"
        qr_img.save(qr_code_path)
        participant.qr_code.save(qr_code_path, open(qr_code_path, 'rb'), save=True)
        participant.save()
        os.remove(qr_code_path)
        return True
    return False