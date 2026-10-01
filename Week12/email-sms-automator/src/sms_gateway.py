from utils import setup_logging
from email_sender import EmailSender

logger = setup_logging(__name__)

class SMSGateway:
    """แปลงข้อความ SMS และส่งผ่าน Email Gateway ของค่ายมือถือ"""
    def __init__(self, email_sender_instance):
        if not isinstance(email_sender_instance, EmailSender):
            raise TypeError("SMSGateway requires an instance of EmailSender.")
        self.email_sender = email_sender_instance
        self.carrier_gateways = {
            "att": "@txt.att.net",
            "verizon": "@vtext.com",
            "tmobile": "@tmomail.net",
            "sprint": "@messaging.sprintpcs.com",
        }
        logger.info("SMSGateway initialized.")

    def send_sms(self, phone_number, message, carrier_name=None):
        sms_gateway_address = None
        if carrier_name and carrier_name.lower() in self.carrier_gateways:
            sms_gateway_address = f"{phone_number}{self.carrier_gateways[carrier_name.lower()]}"
        elif '@' in phone_number and '.' in phone_number:
            sms_gateway_address = phone_number

        if sms_gateway_address:
            logger.info(f"Attempting to send SMS to {phone_number} via {sms_gateway_address}")
            return self.email_sender.send_email(sms_gateway_address, "", message)
        else:
            logger.error("Could not determine SMS gateway address.")
            return False