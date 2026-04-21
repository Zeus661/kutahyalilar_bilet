from app.email import send_email, log_sms


async def handle_booking_created(data: dict):
    ticket_code = data.get("ticket_code", "N/A")
    seat_number = data.get("seat_number", "N/A")
    total_price = data.get("total_price", "N/A")
    subject = f"Biletiniz Onaylandı - {ticket_code}"
    body = (
        f"Sayın Yolcumuz,\n\n"
        f"Biletiniz başarıyla oluşturulmuştur.\n\n"
        f"Bilet Kodu: {ticket_code}\n"
        f"Koltuk No: {seat_number}\n"
        f"Tutar: {total_price} TL\n\n"
        f"İyi yolculuklar dileriz.\n"
        f"Kütahyalılar Turizm"
    )
    await send_email(data.get("email", ""), subject, body)


async def handle_booking_cancelled(data: dict):
    subject = "Biletiniz İptal Edildi"
    body = (
        f"Sayın Yolcumuz,\n\n"
        f"Biletiniz iptal edilmiştir.\n"
        f"İade işleminiz kısa süre içinde tamamlanacaktır.\n\n"
        f"Kütahyalılar Turizm"
    )
    await send_email(data.get("email", ""), subject, body)


async def handle_payment_failed(data: dict):
    subject = "Ödeme Başarısız"
    body = (
        f"Sayın Yolcumuz,\n\n"
        f"Ödemeniz işlenirken bir hata oluştu.\n"
        f"Lütfen tekrar deneyiniz.\n\n"
        f"Hata sebebi: {data.get('failure_reason', 'Bilinmiyor')}\n\n"
        f"Kütahyalılar Turizm"
    )
    await send_email(data.get("email", ""), subject, body)


async def handle_user_registered(data: dict):
    subject = "Kütahyalılar'a Hoşgeldiniz!"
    body = (
        f"Hoşgeldiniz!\n\n"
        f"Kütahyalılar Turizm ailesine katıldığınız için teşekkür ederiz.\n"
        f"Bilet almak için hemen seferlerimize göz atabilirsiniz.\n\n"
        f"Kütahyalılar Turizm"
    )
    await send_email(data.get("email", ""), subject, body)
