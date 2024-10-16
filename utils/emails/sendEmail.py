from jinja2 import Template
from fastapi.responses import JSONResponse
from datetime import datetime
import os, smtplib, ssl, mimetypes
import certifi  # Importamos certifi para manejar los certificados correctamente
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

class CoreMailClient: 

    def __init__(self, smtp_server, port, sender_email,\
                 password, receiver_email:list, subject:str,\
                 message:str, from_name=None):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.password = password
        self.receiver_email = receiver_email
        self.subject = subject
        self.message = message
        self.from_name = from_name
    
    def create_message_text_plain(self):
        message = MIMEText(self.message, 'plain', 'utf-8')
        return message
    
    def create_message_text_html(self):
        message = MIMEText(self.message, 'html', 'utf-8')
        return message

    def create_message_application(self, file_path):
        """Create a message for an email with a file attachment."""
        with open(file_path, "rb") as file:
            mime_type, _ = mimetypes.guess_type(file_path)
            main_type, sub_type = mime_type.split("/", 1) if mime_type else ("application", "octet-stream")
            attachment = MIMEBase(main_type, sub_type)
            attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(file_path)}",
            )
        return attachment

    def get_attachments(self, file_paths:list): 
        attachments = [self.create_message_application(file_path) for file_path in file_paths]
        return tuple(attachments)
 
    def create_message_multipart(self, *attachments):
        message = MIMEMultipart()
        for attachment in attachments:
            message.attach(attachment)
        return message
    
    def get_message(self, *file_paths):
        core_message = self.create_message_text_plain()
        if "</html>" in self.message:
            core_message = self.create_message_text_html()
        message = self.create_message_multipart(core_message, *self.get_attachments(file_paths))
        message["Subject"] = self.subject
        message["From"] = self.from_name if self.from_name else self.sender_email
        message["To"] = ", ".join(self.receiver_email)
        return message
    
    def send_email(self, *file_paths):
        # Usamos el contexto SSL de certifi para los certificados actualizados
        context = ssl.create_default_context(cafile=certifi.where())
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls(context=context)
            server.login(self.sender_email, self.password)
            message = self.get_message(*file_paths)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())
            server.quit()



def sendEmail(name, notificationType, message):
    monthSpanish = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    dateString = f"{datetime.now().day} de {monthSpanish[datetime.now().month - 1]} de {datetime.now().year}"

    # Datos del usuario
    userData = {
        'name': name,
        'notificationType': notificationType,
        'date': dateString ,
        'description': message
    }

    # Cargar el archivo HTML como plantilla
    with open("./utils/emails/index.html", "r", encoding="utf-8") as file:
        templateContent = file.read()

    # Crear una instancia de Template
    template = Template(templateContent)

    # Renderizar el contenido con los datos del usuario
    renderedMessage = template.render(
        Nombre_del_Usuario=userData['name'],
        Tipo_de_Notificación=userData['notificationType'],
        Fecha=userData['date'],
        Descripción_de_la_Notificación=userData['description']
    )

    # Crea una instancia del cliente de correo
    cmClient = CoreMailClient(
        smtp_server="smtp.gmail.com",
        port=587,
        sender_email="morenocordobaalexander00@gmail.com",
        password="odpfegjjitppqeir",
        receiver_email=["alexander.moreno@utp.edu.co"],
        subject="Notificación de BTG Pactual",
        message=renderedMessage,  # Mensaje renderizado
        from_name="Btg Pactual | Notificación"
    )

    # Envía el correo
    cmClient.send_email()  # Envía el correo sin archivos adjuntos
    return JSONResponse(
                status_code=200,
                content={
                    "status": 200,
                    "message": "Operation was successful",
                }
            )