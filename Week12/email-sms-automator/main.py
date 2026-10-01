import sys
import os
import time

# เพิ่มโฟลเดอร์ src เข้าไปใน Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from email_sender import EmailSender
from email_receiver import EmailReceiver
from sms_gateway import SMSGateway
from utils import setup_logging, get_env_variable, ensure_directory_exists

logger = setup_logging(__name__)

def main():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'data')
    attachments_dir = os.path.join(data_dir, 'attachments')
    
    ensure_directory_exists(data_dir)
    ensure_directory_exists(attachments_dir)

    # 1. โหลดข้อมูลจาก .env
    try:
        sender_email = get_env_variable("SENDER_EMAIL")
        sender_app_password = get_env_variable("SENDER_APP_PASSWORD")
        smtp_server = get_env_variable("SMTP_SERVER")
        smtp_port = int(get_env_variable("SMTP_PORT"))
        imap_server = get_env_variable("IMAP_SERVER")

        test_recipient_email = get_env_variable("TEST_RECIPIENT_EMAIL")
        test_sms_phone_number = get_env_variable("TEST_SMS_PHONE_NUMBER")
        test_sms_carrier = get_env_variable("TEST_SMS_CARRIER")
    except ValueError as e:
        logger.critical(f"Configuration error: {e}")
        sys.exit(1)

    # 2. เริ่มทำงาน Object ต่างๆ
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_app_password)
    email_receiver = EmailReceiver(imap_server, sender_email, sender_app_password)
    sms_gateway = SMSGateway(email_sender)

    # Task 1: ส่งข้อความอีเมลแบบข้อความธรรมดา
    logger.info("\n--- Task 1: Sending plain text email ---")
    email_sender.send_email(
        recipient_email=test_recipient_email,
        subject="Automated Python Test Email",
        body="นายปฏิพัฒน์ หอทอง รหัสนักศึกษา 683380424-5"
    )

    # Task 2: ส่งอีเมลพร้อมไฟล์แนบ
    logger.info("\n--- Task 2: Sending email with attachment ---")
    attachment_path = os.path.join(data_dir, 'dummy_report.pdf')
    if os.path.exists(attachment_path):
        email_sender.send_email(
            recipient_email=test_recipient_email,
            subject="Python Test Email with Attachment",
            body="นายปฏิพัฒน์ หอทอง รหัสนักศึกษา 683380424-5",
            attachment_path=attachment_path
        )

    # Task 3: ส่ง SMS
    logger.info("\n--- Task 3: Sending SMS ---")
    sms_gateway.send_sms(
        phone_number=test_sms_phone_number,
        message="นายปฏิพัฒน์ หอทอง รหัสนักศึกษา 683380424-5",
        carrier_name=test_sms_carrier
    )

    # Task 4: รับและประมวลผลอีเมล
    logger.info("\n--- Task 4: Receiving emails ---")
    # ส่งอีเมลหาตัวเองเพื่อใช้ทดสอบรับอีเมล
    email_sender.send_email(
        recipient_email=sender_email,
        subject="Python Test: Email for Receiving Demo",
        body="นายปฏิพัฒน์ หอทอง รหัสนักศึกษา 683380424-5",
        attachment_path=attachment_path
    )

    time.sleep(10) # รอระบบประมวลผลอีเมลสักครู่

    uids = email_receiver.search_emails(
        criteria='UNSEEN',
        from_sender=sender_email,
        subject_contains="Python Test: Email for Receiving Demo"
    )

    if uids:
        for uid in uids:
            details = email_receiver.fetch_email_content(
                uid=uid,
                mark_as_read=True,
                download_attachments_dir=attachments_dir
            )
            if details:
                logger.info(f"From: {details['sender']}")
                logger.info(f"Subject: {details['subject']}")
                logger.info(f"Downloaded attachments: {details['attachments_downloaded']}")

    logger.info("\n--- All tasks completed ---")

if __name__ == "__main__":
    main()