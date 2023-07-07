import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def greetEmail(data: dict) -> bool:
    try:
        msg = MIMEMultipart()

        sender_email = data.get("sender")
        receiver_email = data.get("receiver")
        password = data.get("password")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Welcome to Mili"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        html = (
            """
        <!DOCTYPE html>

        <html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">

        <head>
            <title></title>
            <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
            <meta content="width=device-width, initial-scale=1.0" name="viewport" />
            <!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
            <style>
                * {
                    box-sizing: border-box;
                }

                body {
                    margin: 0;
                    padding: 0;
                }

                a[x-apple-data-detectors] {
                    color: inherit !important;
                    text-decoration: inherit !important;
                }

                #MessageViewBody a {
                    color: inherit;
                    text-decoration: none;
                }

                p {
                    line-height: inherit
                }

                .desktop_hide,
                .desktop_hide table {
                    mso-hide: all;
                    display: none;
                    max-height: 0px;
                    overflow: hidden;
                }

                .image_block img+div {
                    display: none;
                }

                @media (max-width:720px) {

                    .desktop_hide table.icons-inner,
                    .social_block.desktop_hide .social-table {
                        display: inline-block !important;
                    }

                    .icons-inner {
                        text-align: center;
                    }

                    .icons-inner td {
                        margin: 0 auto;
                    }

                    .image_block img.big,
                    .row-content {
                        width: 100% !important;
                    }

                    .mobile_hide {
                        display: none;
                    }

                    .stack .column {
                        width: 100%;
                        display: block;
                    }

                    .mobile_hide {
                        min-height: 0;
                        max-height: 0;
                        max-width: 0;
                        overflow: hidden;
                        font-size: 0px;
                    }

                    .desktop_hide,
                    .desktop_hide table {
                        display: table !important;
                        max-height: none !important;
                    }

                    .row-2 .column-1 .block-3.paragraph_block td.pad>div {
                        font-size: 11px !important;
                    }

                    .row-3 .column-2 .block-1.paragraph_block td.pad>div,
                    .row-5 .column-1 .block-1.paragraph_block td.pad>div,
                    .row-6 .column-2 .block-1.paragraph_block td.pad>div,
                    .row-7 .column-1 .block-2.paragraph_block td.pad>div {
                        font-size: 8px !important;
                    }

                    .row-3 .column-2 .block-1.paragraph_block td.pad,
                    .row-5 .column-1 .block-1.paragraph_block td.pad,
                    .row-6 .column-2 .block-1.paragraph_block td.pad,
                    .row-7 .column-1 .block-2.paragraph_block td.pad {
                        padding: 10px 20px !important;
                    }

                    .row-2 .column-1 .block-1.image_block td.pad {
                        padding: 5px 30px 0 !important;
                    }

                    .row-3 .column-1 .block-1.image_block td.pad,
                    .row-6 .column-1 .block-1.image_block td.pad {
                        padding: 0 0 0 10px !important;
                    }

                    .row-5 .column-2 .block-1.image_block td.pad,
                    .row-7 .column-2 .block-2.image_block td.pad {
                        padding: 0 10px 0 0 !important;
                    }

                    .row-8 .column-1 .block-2.paragraph_block td.pad>div {
                        font-size: 12px !important;
                    }
                }
            </style>
        </head>"""
            + f"""

        <body style="background-color: #ffffff; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
            <table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation"
                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;" width="100%">
                <tbody>
                    <tr>
                        <td>
                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1"
                                role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                                                class="row-content stack" role="presentation"
                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 0; background-color: #28282b; color: #000000; width: 700px;"
                                                width="700">
                                                <tbody>
                                                    <tr>
                                                        <td class="column column-1"
                                                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                                                            width="100%">
                                                            <div class="spacer_block block-1"
                                                                style="height:30px;line-height:30px;font-size:1px;"> </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2"
                                role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                                                class="row-content stack" role="presentation"
                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 0; background-color: #28282b; color: #000000; width: 700px;"
                                                width="700">
                                                <tbody>
                                                    <tr>
                                                        <td class="column column-1"
                                                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                                                            width="100%">
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="image_block block-1" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="width:100%;padding-right:30px;padding-left:30px;">
                                                                        <div align="left" class="alignment"
                                                                            style="line-height:10px"><img
                                                                                src="https://drive.google.com/uc?export=view&id=13l1MqcmDU9Iqsy1yj2mBFqRhyjvvaAja"
                                                                                style="display: block; height: auto; border: 0; width: 100px; max-width: 100%;"
                                                                                width="100" /></div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <div class="spacer_block block-2 mobile_hide"
                                                                style="height:40px;line-height:40px;font-size:1px;"> </div>
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="paragraph_block block-3" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:10px;">
                                                                        <div
                                                                            style="color:#ffffff;direction:ltr;font-family:Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;font-size:15px;font-weight:700;letter-spacing:0px;line-height:150%;text-align:left;mso-line-height-alt:22.5px;">
                                                                            <p style="margin: 0; margin-bottom: 0px;">Hello
                                                                                {data.get("name")},</p>
                                                                            <p style="margin: 0; margin-bottom: 0px;">We are
                                                                                almost done creating your account. Thanks for
                                                                                signing into Mili on your Windows device. You
                                                                                can use this account to use Mili Assistant.
                                                                                Please read the terms and consitions carefully.
                                                                            </p>
                                                                            <p style="margin: 0; margin-bottom: 0px;">Thanks and
                                                                                Regards,</p>
                                                                            <p style="margin: 0;">Your Mili Assistant.</p>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <div class="spacer_block block-4 mobile_hide"
                                                                style="height:20px;line-height:20px;font-size:1px;"> </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3"
                                role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content"
                                                role="presentation"
                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 0; background-color: #28282b; color: #000000; width: 700px;"
                                                width="700">
                                                <tbody>
                                                    <tr>
                                                        <td class="column column-1"
                                                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                                                            width="50%">
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="image_block block-1" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="width:100%;padding-left:30px;padding-right:0px;">
                                                                        <div align="center" class="alignment"
                                                                            style="line-height:10px"><img class="big"
                                                                                src="https://drive.google.com/uc?export=view&id=16DBVUgV-gZzrw58jkpJev7zBUrt9PVVt"
                                                                                style="display: block; height: auto; border: 0; width: 350px; max-width: 100%;"
                                                                                width="350" /></div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                        <td class="column column-2"
                                                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                                                            width="50%">
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="paragraph_block block-1" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="padding-bottom:10px;padding-left:20px;padding-right:30px;padding-top:40px;">
                                                                        <div
                                                                            style="color:#ffffff;direction:ltr;font-family:'Helvetica Neue', Helvetica, Arial, sans-serif;font-size:13px;font-weight:400;letter-spacing:0px;line-height:150%;text-align:right;mso-line-height-alt:19.5px;">
                                                                            <p style="margin: 0; margin-bottom: 14px;">From
                                                                                chole bhature to pani puri, ignite your senses
                                                                                with flavourful dishes that'll transport you
                                                                                through Northern India.</p>
                                                                            <p style="margin: 0;">"Take me to Jwalapur"</p>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4"
                                role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                                                class="row-content stack" role="presentation"
                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 0; background-color: #28282b; color: #000000; width: 700px;"
                                                width="700">
                                                <tbody>
                                                    <tr>
                                                        <td class="column column-1"
                                                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                                                            width="100%">
                                                            <div class="spacer_block block-1"
                                                                style="height:25px;line-height:25px;font-size:1px;"> </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-5"
                                role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content"
                                                role="presentation"
                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 0; background-color: #28282b; color: #000000; width: 700px;"
                                                width="700">
                                                <tbody>
                                                    <tr>
                                                        <td class="column column-1"
                                                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                                                            width="50%">
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="paragraph_block block-1" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="padding-bottom:10px;padding-left:20px;padding-right:20px;padding-top:40px;">
                                                                        <div
                                                                            style="color:#ffffff;direction:ltr;font-family:'Helvetica Neue', Helvetica, Arial, sans-serif;font-size:14px;font-weight:400;letter-spacing:0px;line-height:150%;text-align:left;mso-line-height-alt:21px;">
                                                                            <p style="margin: 0; margin-bottom: 16px;">Indulge
                                                                                in rasgullas from Kolkata or homemade ghewar
                                                                                from Rajasthan, and share some sweetness with
                                                                                the ones you love.</p>
                                                                            <p style="margin: 0;">"Where to eat ghewar ?"</p>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                        <td class="column column-2"
                                                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                                                            width="50%">
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="image_block block-1" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="width:100%;padding-right:30px;padding-left:0px;">
                                                                        <div align="center" class="alignment"
                                                                            style="line-height:10px"><img class="big"
                                                                                src="https://drive.google.com/uc?export=view&id=18mz6WPf9RhMDz4KW4OprOhW6CAYC0Dg0"
                                                                                style="display: block; height: auto; border: 0; width: 350px; max-width: 100%;"
                                                                                width="350" /></div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <div class="spacer_block block-2"
                                                                style="height:25px;line-height:25px;font-size:1px;"> </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-6"
                                role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content"
                                                role="presentation"
                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 0; background-color: #28282b; color: #000000; width: 700px;"
                                                width="700">
                                                <tbody>
                                                    <tr>
                                                        <td class="column column-1"
                                                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                                                            width="50%">
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="image_block block-1" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="width:100%;padding-left:30px;padding-right:0px;">
                                                                        <div align="center" class="alignment"
                                                                            style="line-height:10px"><img
                                                                                src="https://drive.google.com/uc?export=view&id=1MmRHRxelWrVOHPgDIu-oq9vN8I_y18Ub"
                                                                                style="display: block; height: auto; border: 0; width: 320px; max-width: 100%;"
                                                                                width="320" /></div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                        <td class="column column-2"
                                                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                                                            width="50%">
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="paragraph_block block-1" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="padding-bottom:10px;padding-left:35px;padding-right:30px;padding-top:40px;">
                                                                        <div
                                                                            style="color:#ffffff;direction:ltr;font-family:'Helvetica Neue', Helvetica, Arial, sans-serif;font-size:13px;font-weight:400;letter-spacing:0px;line-height:150%;text-align:right;mso-line-height-alt:19.5px;">
                                                                            <p style="margin: 0; margin-bottom: 14px;">         
                                                                                   Open your favorite apps and websites by your
                                                                                voice</p>
                                                                            <p style="margin: 0;">"Just say open spotify"</p>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-7"
                                role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content"
                                                role="presentation"
                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 0; background-color: #28282b; color: #000000; width: 700px;"
                                                width="700">
                                                <tbody>
                                                    <tr>
                                                        <td class="column column-1"
                                                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                                                            width="50%">
                                                            <div class="spacer_block block-1"
                                                                style="height:25px;line-height:25px;font-size:1px;"> </div>
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="paragraph_block block-2" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="padding-bottom:10px;padding-left:20px;padding-right:20px;padding-top:40px;">
                                                                        <div
                                                                            style="color:#ffffff;direction:ltr;font-family:'Helvetica Neue', Helvetica, Arial, sans-serif;font-size:14px;font-weight:400;letter-spacing:0px;line-height:150%;text-align:left;mso-line-height-alt:21px;">
                                                                            <p style="margin: 0; margin-bottom: 16px;">With your
                                                                                Mili Assistant, you can ask the current weather
                                                                                and upcoming forecast for your location using
                                                                                your voice .</p>
                                                                            <p style="margin: 0;">"What's today weather ?"</p>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                        <td class="column column-2"
                                                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                                                            width="50%">
                                                            <div class="spacer_block block-1"
                                                                style="height:25px;line-height:25px;font-size:1px;"> </div>
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="image_block block-2" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="width:100%;padding-right:30px;padding-left:0px;">
                                                                        <div align="center" class="alignment"
                                                                            style="line-height:10px"><img
                                                                                src="https://drive.google.com/uc?export=view&id=1p8Wybn5gWOOdLrI4a2oiGgPSSRnxstYj"
                                                                                style="display: block; height: auto; border: 0; width: 320px; max-width: 100%;"
                                                                                width="320" /></div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <div class="spacer_block block-3"
                                                                style="height:25px;line-height:25px;font-size:1px;"> </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-8"
                                role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-size: auto;"
                                width="100%">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content"
                                                role="presentation"
                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-size: auto; border-radius: 0; background-color: #28282b; color: #000000; width: 700px;"
                                                width="700">
                                                <tbody>
                                                    <tr>
                                                        <td class="column column-1"
                                                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                                                            width="100%">
                                                            <div class="spacer_block block-1"
                                                                style="height:25px;line-height:25px;font-size:1px;"> </div>
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="paragraph_block block-2" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:10px;">
                                                                        <div
                                                                            style="color:#ffffff;direction:ltr;font-family:Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;font-size:14px;font-weight:400;letter-spacing:0px;line-height:150%;text-align:justify;mso-line-height-alt:21px;">
                                                                            <p style="margin: 0;">This informational email was
                                                                                sent to <a
                                                                                    href="mailto:yourvirtualmiliassistant@gmail.com"
                                                                                    rel="noopener"
                                                                                    style="text-decoration: underline; color: #ffffff;"
                                                                                    target="_blank">shivamrai072002@gmail.com</a>
                                                                                because you recently signed into your Mili
                                                                                Account on your Windows Device. If you do not
                                                                                wish to receive emails to help you set up your
                                                                                device with Mili when you signed into your
                                                                                account on the device for the first time, please
                                                                                <a href="http://www.example.com" rel="noopener"
                                                                                    style="text-decoration: underline; color: #ffffff;"
                                                                                    target="_blank">Unsubscribe</a></p>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="social_block block-3" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="padding-bottom:20px;padding-left:10px;padding-right:10px;padding-top:20px;text-align:center;">
                                                                        <div align="center" class="alignment">
                                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                                class="social-table" role="presentation"
                                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; display: inline-block;"
                                                                                width="208px">
                                                                                <tr>
                                                                                    <td style="padding:0 10px 0 10px;"><a
                                                                                            href="https://www.twitter.com/"
                                                                                            target="_blank"><img alt="twitter"
                                                                                                height="32"
                                                                                                src="https://drive.google.com/uc?export=view&id=1CEME_BDDDmgg5kcNMJ05rp1nx2EQ6bLF"
                                                                                                style="display: block; height: auto; border: 0;"
                                                                                                title="twitter"
                                                                                                width="32" /></a></td>
                                                                                    <td style="padding:0 10px 0 10px;"><a
                                                                                            href="https://www.linkedin.com/"
                                                                                            target="_blank"><img alt="linkedin"
                                                                                                height="32"
                                                                                                src="https://drive.google.com/uc?export=view&id=1mQ9QU8b3sdFoVn2amBowWMuyQICsYBe2"
                                                                                                style="display: block; height: auto; border: 0;"
                                                                                                title="linkedin"
                                                                                                width="32" /></a></td>
                                                                                    <td style="padding:0 10px 0 10px;"><a
                                                                                            href="https://www.instagram.com/miliassistant/"
                                                                                            target="_blank"><img alt="instagram"
                                                                                                height="32"
                                                                                                src="https://drive.google.com/uc?export=view&id=1pDV9OtR0Fcuz9kesHoo957uuFtO6ts8Z"
                                                                                                style="display: block; height: auto; border: 0;"
                                                                                                title="instagram"
                                                                                                width="32" /></a></td>
                                                                                    <td style="padding:0 10px 0 10px;"><a
                                                                                            href="t.me/miliassistantbot"
                                                                                            target="_blank"><img alt="Telegram"
                                                                                                height="32"
                                                                                                src="https://drive.google.com/uc?export=view&id=1ut_h1VINKSe870S3P8weUsIOlHeD-WvL"
                                                                                                style="display: block; height: auto; border: 0;"
                                                                                                title="Telegram"
                                                                                                width="32" /></a></td>
                                                                                </tr>
                                                                            </table>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                class="paragraph_block block-4" role="presentation"
                                                                style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
                                                                width="100%">
                                                                <tr>
                                                                    <td class="pad"
                                                                        style="padding-bottom:20px;padding-left:20px;padding-right:20px;padding-top:10px;">
                                                                        <div
                                                                            style="color:#ffffff;direction:ltr;font-family:'Helvetica Neue', Helvetica, Arial, sans-serif;font-size:14px;font-weight:400;letter-spacing:0px;line-height:150%;text-align:center;mso-line-height-alt:21px;">
                                                                            <p style="margin: 0;">Mili Assistant |
                                                                                Haridwar, Uttarakhand<br />Post Code 249402</p>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table><!-- End -->
        </body>

        </html>
        """
        )

        body = MIMEText(html, "html")
        msg.attach(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

    except:
        return False
