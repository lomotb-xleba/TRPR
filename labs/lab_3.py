import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging

class YandexMailBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.smtp_server = "smtp.yandex.ru"
        self.smtp_port = 587
        self.imap_server = "imap.yandex.ru"
        self.imap_port = 993
        
        # Настройка логирования
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

#Отправка письма с HTML-форматированием и вложением---------------------------------------
    def send_email_with_attachment(self, to_email, subject, html_content, attachment_path):
        try:
            # Создание сообщения
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject

            # Добавление HTML-части
            msg.attach(MIMEText(html_content, 'html'))

            # Добавление вложения
            if os.path.exists(attachment_path):
                attachment = MIMEBase('application', 'octet-stream')
                with open(attachment_path, 'rb') as file:
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{os.path.basename(attachment_path)}"'
                )
                msg.attach(attachment)
                self.logger.info(f"Вложение добавлено: {attachment_path}")
            else:
                self.logger.warning(f"Файл вложения не найден: {attachment_path}")

            # Отправка через SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
                self.logger.info(f"Письмо успешно отправлено на {to_email}")

        except Exception as e:
            self.logger.error(f"Ошибка при отправке письма: {e}")

#Подключение к IMAP серверу----------------------------------------------------
    def connect_imap(self):
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email, self.password)
            self.logger.info("Успешное подключение к IMAP серверу")
            return mail
        except Exception as e:
            self.logger.error(f"Ошибка подключения к IMAP: {e}")
            return None

    def search_emails_with_attachments(self, mail, folder='INBOX'):
        """
        Поиск писем с вложениями
        """
        try:
            mail.select(folder)
            
            # Поиск всех непрочитанных писем
            result, data = mail.search(None, 'UNSEEN')
            email_ids = data[0].split()
            
            emails_with_attachments = []
            
            for email_id in email_ids:
                # Получение письма
                result, data = mail.fetch(email_id, '(RFC822)')
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                # Проверка на наличие вложений
                if self.has_attachments(msg):
                    email_info = {
                        'id': email_id,
                        'subject': msg['subject'],
                        'from': msg['from'],
                        'date': msg['date'],
                        'message': msg
                    }
                    emails_with_attachments.append(email_info)
                    self.logger.info(f"Найдено письмо с вложением: {msg['subject']}")
            
            return emails_with_attachments
            
        except Exception as e:
            self.logger.error(f"Ошибка при поиске писем: {e}")
            return []
        
#Проверка наличия вложений в письме-------------------------------------------
    def has_attachments(self, msg):
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                return True
        return False

#Пометить письмо как прочитанное----------------------------------------------
    def mark_as_read(self, mail, email_id):
        try:
            mail.store(email_id, '+FLAGS', '\\Seen')
            self.logger.info(f"Письмо {email_id} помечено как прочитанное")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при отметке письма как прочитанного: {e}")
            return False
        
#Основная функция обработки входящих писем-----------------------------------
    def process_incoming_emails(self):
        self.logger.info("Начало обработки входящих писем")
        
        mail = self.connect_imap()
        if not mail:
            return

        try:
            # Поиск писем с вложениями
            emails_with_attachments = self.search_emails_with_attachments(mail)
            
            # Обработка найденных писем
            for email_info in emails_with_attachments:
                self.logger.info(f"Обработка письма: {email_info['subject']}")
                
                # Пометить как прочитанное
                self.mark_as_read(mail, email_info['id'])
                
                # Здесь можно добавить дополнительную логику обработки
                # Например, сохранение вложений, анализ содержимого и т.д.
                
            self.logger.info(f"Обработано писем с вложениями: {len(emails_with_attachments)}")
            
        finally:
            mail.close()
            mail.logout()

def main():
#ФИКСИРОВАННЫЕ ДАННЫЕ (Параметр 3)
    YANDEX_EMAIL = "tomochka.da@yandex.ru" 
    YANDEX_PASSWORD = "bmivneeyeapbicdk"  
    
    mail_bot = YandexMailBot(YANDEX_EMAIL, YANDEX_PASSWORD)
    
#Пример отправки письма с HTML и вложением (Параметр 2)
    html_content = """
    <html>
        <head></head>
        <body>
            <h1 style="color: #ff0000;">Важное письмо</h1>
            <p>Это <b>HTML-письмо</b> с вложением.</p>
            <p>Отправлено автоматически через Python-бота.</p>
        </body>
    </html>
    """
    
    # Отправка тестового письма
    mail_bot.send_email_with_attachment(
        to_email="tomochkada@gmail.com", 
        subject="Тестовое письмо с вложением",
        html_content=html_content,
        attachment_path="labs\example.txt"
    )
    
#Обработка входящих писем (Параметры 4 и 5)
    mail_bot.process_incoming_emails()

if __name__ == "__main__":
    main()