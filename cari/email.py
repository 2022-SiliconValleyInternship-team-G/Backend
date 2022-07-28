from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives


# the function for sending an email
def send_email(recipient, image_path_list):

    subject = "View your generated caricature!" #주제
    html_message = f"""
    <!doctype html>
        <html lang=en>
            <head>
                <meta charset=utf-8>
                <title>Some title.</title>
            </head>
            <body>
                <h1>{subject}</h1>
                <p>
                Here is the generated caricature. Thank you! <br>
                <img src='cid:{Path(image_path_list[0]).name}'/>
                <img src='cid:{Path(image_path_list[1]).name}'/>
                <img src='cid:{Path(image_path_list[2]).name}'/>
                <img src='cid:{Path(image_path_list[3]).name}'/>
                <img src='cid:{Path(image_path_list[4]).name}'/>
                <img src='cid:{Path(image_path_list[5]).name}'/>
                <img src='cid:{Path(image_path_list[6]).name}'/>
                <img src='cid:{Path(image_path_list[7]).name}'/>
                </p>
            </body>
        </html>
    """
    email = EmailMultiAlternatives(subject=subject,
                                to=recipient if isinstance(recipient, list) else [recipient])

    if all([html_message]):
        email.attach_alternative(html_message, "text/html")
        email.content_subtype = 'html'  # set the primary content to be text/html
        email.mixed_subtype = 'related' # it is an important part that ensures embedding of an image

        for item in image_path_list:
            image_path = "/home/teamg/volume/CarryCARI-BE{path}".format(path = item)
            image_name = Path(image_path).name
            with open(image_path, mode='rb') as f:
                image = MIMEImage(f.read())
                email.attach(image)
                image.add_header('Content-ID', f"<{image_name}>")

    email.send()
