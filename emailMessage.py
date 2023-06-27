import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox


class MailToUser:
    def __init__(self, data):
        self.data = data

    def greetingMail(self):
        try:
            sender_email = self.data.get("sender")
            receiver_email = self.data.get("receiver")
            password = self.data.get("password")

            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Welcome to Mili"
            msg["From"] = sender_email
            msg["To"] = receiver_email
            filename = "Terms and conditions.pdf"

            html = """\
			<!DOCTYPE html>

			<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">

			<head>
				<title></title>
				<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
				<meta content="width=device-width, initial-scale=1.0" name="viewport" />
				<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
				<!--[if !mso]><!-->
				<link href="https://fonts.googleapis.com/css?family=Abril+Fatface" rel="stylesheet" type="text/css" />
				<link href="https://fonts.googleapis.com/css?family=Catamaran" rel="stylesheet" type="text/css" />
				<link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet" type="text/css" />
				<link href="https://fonts.googleapis.com/css?family=Droid+Serif" rel="stylesheet" type="text/css" />
				<link href="https://fonts.googleapis.com/css?family=Nunito" rel="stylesheet" type="text/css" />
				<!--<![endif]-->
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

					@media (max-width:700px) {
						.desktop_hide table.icons-inner {
							display: inline-block !important;
						}

						.icons-inner {
							text-align: center;
						}

						.icons-inner td {
							margin: 0 auto;
						}

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

						.row-2 .column-1 .block-2.paragraph_block td.pad>div {
							font-size: 53px !important;
						}

						.row-4 .column-1 .block-2.paragraph_block td.pad>div {
							font-size: 58px !important;
						}
					}
				</style>
			</head>"""+f"""
			<body style="background-color: #ffffff; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
				<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation"
					style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;" width="100%">
					<tbody>
						<tr>
							<td>
								<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1"
									role="presentation"
									style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #28282b; background-position: top center;"
									width="100%">
									<tbody>
										<tr>
											<td>
												<table align="center" border="0" cellpadding="0" cellspacing="0"
													class="row-content stack" role="presentation"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #28282b; color: #000000; width: 680px;"
													width="680">
													<tbody>
														<tr>
															<td class="column column-1"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
																width="100%">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="heading_block block-2" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																	width="100%">
																	<tr>
																		<td class="pad"
																			style="width:100%;text-align:center;padding-top:25px;">
																			<h1
																				style="margin: 0; color: #555555; font-size: 35px; font-family: Nunito, Arial, Helvetica Neue, Helvetica, sans-serif; line-height: 120%; text-align: center; direction: ltr; font-weight: 700; letter-spacing: normal; margin-top: 0; margin-bottom: 0;">
																				<span class="tinyMce-placeholder"><span
																						style="color: #00a5ff;">M<span
																							style="color: #ff0038;">i<span
																								style="color: #f6ff00;">l<span
																									style="color: #23d435;">i</span></span></span></span></span>
																			</h1>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="text_block block-3" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td class="pad"
																			style="padding-bottom:45px;padding-left:30px;padding-right:30px;padding-top:10px;">
																			<div style="font-family: Arial, sans-serif">
																				<div class=""
																					style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #dfdedc; line-height: 1.2; font-family: 'Nunito', Arial, 'Helvetica Neue', Helvetica, sans-serif;">
																					<p
																						style="margin: 0; font-size: 13px; mso-line-height-alt: 14.399999999999999px;">
																						 </p>
																					<p
																						style="margin: 0; font-size: 13px; mso-line-height-alt: 15.6px;">
																						<span style="font-size:13px;">Hello {self.data["name"]},</span>
																					</p>
																					<p
																						style="margin: 0; font-size: 13px; mso-line-height-alt: 14.399999999999999px;">
																						 </p>
																					<p
																						style="margin: 0; font-size: 13px; mso-line-height-alt: 15.6px;">
																						<span style="font-size:13px;">We are almost
																							done creating your account. Thanks for
																							signing into Mili on your Windows
																							device. You can use this account to use
																							Mili Assistant. Please read the terms
																							and conditions carefully.</span></p>
																					<p
																						style="margin: 0; font-size: 13px; mso-line-height-alt: 15.6px;">
																						<span style="font-size:13px;">Thanks &
																							Regards,</span></p>
																					<p
																						style="margin: 0; font-size: 13px; mso-line-height-alt: 15.6px;">
																						<span style="font-size:13px;">Your Mili
																							Assistant</span></p>
																				</div>
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
								<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2"
									role="presentation"
									style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #616247;" width="100%">
									<tbody>
										<tr>
											<td>
												<table align="center" border="0" cellpadding="0" cellspacing="0"
													class="row-content stack" role="presentation"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-position: top center; background-color: #616247; color: #000000; width: 680px;"
													width="680">
													<tbody>
														<tr>
															<td class="column column-1"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
																width="50%">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="paragraph_block block-2" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td class="pad"
																			style="padding-top:15px;padding-right:10px;padding-bottom:15px;padding-left:10px;">
																			<div
																				style="color:#000000;font-size:55px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:66px;">
																				<p style="margin: 0;">🍿🍩🍰🍹</p>
																			</div>
																		</td>
																	</tr>
																</table>
															</td>
															<td class="column column-2"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
																width="50%">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="paragraph_block block-2" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td class="pad"
																			style="padding-top:15px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
																			<div
																				style="color:#ffffff;font-size:12px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:14.399999999999999px;">
																				<p style="margin: 0;"><strong>Indulge in rasgullas
																						from </strong><strong>Kolkata or
																						homemade</strong><br /><strong>ghewar from
																						Rajasthan, and </strong><strong>share some
																						sweetness</strong><br /><strong>with the
																						ones you love.</strong></p>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="paragraph_block block-3" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td class="pad"
																			style="padding-right:10px;padding-bottom:15px;padding-left:10px;">
																			<div
																				style="color:#ffffff;font-size:14px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:16.8px;">
																				<p style="margin: 0;"><strong>"Where to eat
																						ghewar?"</strong></p>
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
								<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3"
									role="presentation"
									style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #616247;" width="100%">
									<tbody>
										<tr>
											<td>
												<table align="center" border="0" cellpadding="0" cellspacing="0"
													class="row-content stack" role="presentation"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 680px;"
													width="680">
													<tbody>
														<tr>
															<td class="column column-1"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
																width="100%">
																<div class="spacer_block"
																	style="height:1px;line-height:1px;font-size:1px;"> </div>
															</td>
														</tr>
													</tbody>
												</table>
											</td>
										</tr>
									</tbody>
								</table>
								<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4"
									role="presentation"
									style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #616247;" width="100%">
									<tbody>
										<tr>
											<td>
												<table align="center" border="0" cellpadding="0" cellspacing="0"
													class="row-content stack" role="presentation"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #616247; color: #000000; border-radius: 0; width: 680px;"
													width="680">
													<tbody>
														<tr>
															<td class="column column-1"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
																width="50%">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="paragraph_block block-2" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td class="pad"
																			style="padding-top:15px;padding-right:10px;padding-bottom:15px;padding-left:10px;">
																			<div
																				style="color:#000000;font-size:53px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:63.599999999999994px;">
																				<p style="margin: 0;">⛅☀️🌧☔</p>
																			</div>
																		</td>
																	</tr>
																</table>
															</td>
															<td class="column column-2"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
																width="50%">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="paragraph_block block-2" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td class="pad"
																			style="padding-top:15px;padding-right:10px;padding-bottom:30px;padding-left:10px;">
																			<div
																				style="color:#ffffff;font-size:13px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:15.6px;">
																				<p style="margin: 0;"><strong>With your
																					</strong><strong>you can the
																					</strong><strong>current weather
																						and</strong><br /><strong>upcoming forecast
																					</strong><strong>for your location
																					</strong><strong>using only your voice.
																					</strong><strong>Mili assistant</strong></p>
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
								<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-5"
									role="presentation"
									style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #28282b;" width="100%">
									<tbody>
										<tr>
											<td>
												<table align="center" border="0" cellpadding="0" cellspacing="0"
													class="row-content stack" role="presentation"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #28282b; color: #000000; width: 680px;"
													width="680">
													<tbody>
														<tr>
															<td class="column column-1"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 0px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
																width="100%">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="paragraph_block block-2" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td class="pad"
																			style="padding-top:50px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
																			<div
																				style="color:#000000;font-size:13px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:15.6px;">
																				<p style="margin: 0;"><span
																						style="color: #ffffff;">Do you like this
																						mail?</span></p>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="10" cellspacing="0"
																	class="paragraph_block block-3" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td class="pad">
																			<div
																				style="color:#000000;font-size:23px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:27.599999999999998px;">
																				<p style="margin: 0;">😃 😐 🙄 🙁</p>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="text_block block-4" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td class="pad"
																			style="padding-bottom:10px;padding-left:20px;padding-right:20px;padding-top:10px;">
																			<div style="font-family: Arial, sans-serif">
																				<div class=""
																					style="font-size: 12px; mso-line-height-alt: 18px; color: #f8fafe; line-height: 1.5; font-family: 'Nunito', Arial, 'Helvetica Neue', Helvetica, sans-serif;">
																					<p
																						style="margin: 0; font-size: 12px; text-align: justify; mso-line-height-alt: 18px; letter-spacing: normal;">
																						This informational email was sent to <a
																							href="mailto:yourvirtualmiliassistant@gmail.com"
																							rel="noreferrer noopener"
																							style="text-decoration: underline; color: #f8fafe;"
																							target="_blank">{receiver_email}</a> because
																						you recently signed into your Mili Account
																						on your Windows device. If you do not wish
																						to receive emails to help you set up your
																						device with Mili when you sign into your
																						account on the device for the first time,
																						please <a
																							href="https://notifications.google.com/g/p/AM0Overow5ujbfc6GfJvWEYjJXuqrJNhtY2zG3LQbeAX97iOjhUY2nMR3_MkG3RGdMyWcpNVu0uQfvOX6s8O1h1wcAXdzeujV9lf0qYnxiqULlkyYnE0BoOhX3gxZ9PYVTB9lerxI_2fxbgPlIPMwT3zfw_p9sBBgevR565SlQrLYgLpqUri39nHIhzziYSO6RqRYO9qGvRnCU7YZ1UNwqcvH4BNs1lELDJVMLfcD9LAdk_xXzd65u4CUCnFFMJkoqOyQoansPVw720hgLBcJhK3A1VyPY1ZfmI1bPjYHUxmOiZbKX8HHo8UpmTJH72C5_xRZM_iO4jfLfyIqpTNfOP34MjW7bfiidtkc45lXn1QY5WzmBt2XHBCM0DKY80ezojT72F4lSsMC38VRCsw9-VhmqX-HAbaJ1I4WyDbm5PbOG9hWxexOGtPLtLkAStBOQBVxzn5AMY6m0mWyh4e2YEX71W2eWbQk46hDRg95HBhoyJ5kh6GTsuT9iPOEk5Ptk0o7mnPv6I4v97KFnDfkPk2OFbJce48su7c7kTkpmzkoVCmZl8YZEH4goGYum-0SY4"
																							rel="noreferrer noopener"
																							style="text-decoration: underline; color: #f8fafe;"
																							target="_blank">unsubscribe</a></p>
																				</div>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="10" cellspacing="0"
																	class="text_block block-5" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																	width="100%">
																	<tr>
																		<td class="pad">
																			<div style="font-family: sans-serif">
																				<div class=""
																					style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #f8fafe; line-height: 1.2; font-family: Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;">
																					<p
																						style="margin: 0; font-size: 12px; text-align: center; mso-line-height-alt: 14.399999999999999px;">
																						Copyright © 2023 Mili Assistant, All rights
																						reserved.</p>
																				</div>
																			</div>
																		</td>
																	</tr>
																</table>
																<table border="0" cellpadding="0" cellspacing="0"
																	class="html_block block-6" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																	width="100%">
																	<tr>
																		<td class="pad">
																			<div align="center"
																				style="font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;text-align:center;">
																				<div style="height-top: 20px;"> </div>
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
								<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-6"
									role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
									<tbody>
										<tr>
											<td>
												<table align="center" border="0" cellpadding="0" cellspacing="0"
													class="row-content stack" role="presentation"
													style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 680px;"
													width="680">
													<tbody>
														<tr>
															<td class="column column-1"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
																width="100%">
																<table border="0" cellpadding="0" cellspacing="0"
																	class="icons_block block-1" role="presentation"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																	width="100%">
																	<tr>
																		<td class="pad"
																			style="vertical-align: middle; color: #9d9d9d; font-family: inherit; font-size: 15px; padding-bottom: 5px; padding-top: 5px; text-align: center;">
																			<table cellpadding="0" cellspacing="0"
																				role="presentation"
																				style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																				width="100%">
																				<tr>
																					<td class="alignment"
																						style="vertical-align: middle; text-align: center;">
																						<!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
																						<!--[if !vml]><!-->
																					</td>
																				</tr>
																			</table>
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

            part = MIMEText(html, "html")
            msg.attach(part)

            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                "attachment", filename=filename
            )
            msg.attach(part)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, msg.as_string()
                )
        except:
            messagebox.showerror("Mili", "Connection error\nTry Again")

    def sendOTP(self):
        try:
            sender_email = self.data.get("sender")
            receiver_email = self.data.get("receiver")
            password = self.data.get("password")
            otp = self.data.get("otp")

            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"{otp} is your Mili code"
            msg["From"] = sender_email
            msg["To"] = receiver_email
            html = """\
				<!DOCTYPE html>

				<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">

				<head>
					<title></title>
					<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
					<meta content="width=device-width, initial-scale=1.0" name="viewport" />

					<link href="https://fonts.googleapis.com/css?family=Nunito" rel="stylesheet" type="text/css" />
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

						@media (max-width:760px) {
							.desktop_hide table.icons-inner {
								display: inline-block !important;
							}

							.icons-inner {
								text-align: center;
							}

							.icons-inner td {
								margin: 0 auto;
							}

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

							.row-1 .column-1 .block-2.heading_block h1 {
								font-size: 27px !important;
							}
						}
					</style>
				</head>"""+f"""

				<body style="background-color: #ffffff; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
					<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation"
						style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;" width="100%">
						<tbody>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1"
										role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #28282b; background-position: top center;"
										width="100%">
										<tbody>
											<tr>
												<td>
													<table align="center" border="0" cellpadding="0" cellspacing="0"
														class="row-content stack" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #28282b; color: #000000; width: 740px;"
														width="740">
														<tbody>
															<tr>
																<td class="column column-1"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
																	width="100%">
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="heading_block block-2" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="width:100%;text-align:center;padding-left:25px;padding-top:23px;">
																				<h1
																					style="margin: 0; color: #555555; font-size: 27px; font-family: Nunito, Arial, Helvetica Neue, Helvetica, sans-serif; line-height: 120%; text-align: left; direction: ltr; font-weight: 700; letter-spacing: normal; margin-top: 0; margin-bottom: 0;">
																					<span class="tinyMce-placeholder">MILI</span></h1>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="text_block block-3" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:10px;">
																				<div style="font-family: sans-serif">
																					<div class=""
																						style="font-size: 12px; font-family: Nunito, Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #dfdedc; line-height: 1.2;">
																						<p
																							style="margin: 0; text-align: justify; mso-line-height-alt: 14.399999999999999px;">
																							<strong>Hi,</strong></p>
																						<p
																							style="margin: 0; text-align: justify; mso-line-height-alt: 14.399999999999999px;">
																							<strong>Someone tried to sign up for an
																								Mili account with
																								{receiver_email}. If it was
																								you, enter this confirmation code in the
																								app:</strong></p>
																						<p
																							style="margin: 0; font-size: 12px; mso-line-height-alt: 14.399999999999999px;">
																							 </p>
																					</div>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="5" cellspacing="0"
																		class="heading_block block-4" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="pad">
																				<h1
																					style="margin: 0; color: #555555; font-size: 30px; font-family: Nunito, Arial, Helvetica Neue, Helvetica, sans-serif; line-height: 120%; text-align: center; direction: ltr; font-weight: 700; letter-spacing: normal; margin-top: 0; margin-bottom: 0;">
																					<span class="tinyMce-placeholder">{otp}</span></h1>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="paragraph_block block-5" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-top:10px;padding-right:30px;padding-bottom:10px;padding-left:25px;">
																				<div
																					style="color:#ffffff;font-size:11px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:700;line-height:120%;text-align:justify;direction:ltr;letter-spacing:0px;mso-line-height-alt:13.2px;">
																					<p style="margin: 0;">Please note that this OTP will
																						only be valid for a limited period, so we kindly
																						request you to use it promptly to avoid any
																						inconvenience. Do not disclose OTP. If not done
																						by you, report on <a
																							href="mailto:yourvirtualmiliassistant@gmail.com?subject=Email%20regarding%20%20about%20Unauthorized%20Access%20Attempts"
																							rel="noopener"
																							style="text-decoration: underline; color: #1ea08b;"
																							target="_blank"
																							title="yourvirtualmiliassistant@gmail.com">yourvirtualmiliassistant@gmail.com</a> 
																						as FRAUD. We solicit your continued patronage to
																						our service.</p>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="2" cellspacing="0"
																		class="paragraph_block block-6" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad">
																				<div
																					style="color:#555555;font-size:9px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:10.799999999999999px;">
																					<p style="margin: 0;">from<span
																							style="color: #00a5ff;"></span></p>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="paragraph_block block-7" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad" style="padding-bottom:35px;">
																				<div
																					style="color:#000000;font-size:11px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:13.2px;">
																					<p style="margin: 0;"><strong><span
																								style="color: #00a5ff;">M<span
																									style="color: #ff0038;">i<span
																										style="color: #f6ff00;">l<span
																											style="color: #23d435;">i</span></span></span></span></strong>
																					</p>
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
					</table>
				</body>
				</html>
				"""
            part = MIMEText(html, "html")
            msg.attach(part)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, msg.as_string()
                )
        except Exception as e:
            messagebox.showerror("Mili", "Connection error\nTry Again")

    def loginWarning(self):
        try:
            sender_email = self.data.get("sender")
            receiver_email = self.data.get("receiver")
            password = self.data.get("password")
            location = self.data.get("location")
            device = self.data.get("device")

            msg = MIMEMultipart("alternative")
            msg["Subject"] = "New login to Mili on Windows"
            msg["From"] = sender_email
            msg["To"] = receiver_email

            html = """\
				<!DOCTYPE html>

				<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">

				<head>
					<title></title>
					<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
					<meta content="width=device-width, initial-scale=1.0" name="viewport" />

					<link href="https://fonts.googleapis.com/css?family=Nunito" rel="stylesheet" type="text/css" />

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

						@media (max-width:920px) {
							.desktop_hide table.icons-inner {
								display: inline-block !important;
							}

							.icons-inner {
								text-align: center;
							}

							.icons-inner td {
								margin: 0 auto;
							}

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
						}

						@media (max-width:768px) {
							.row-1 .column-1 .block-1.heading_block td.pad {
								padding: 15px 30px 0 !important;
							}

							.row-1 .column-1 .block-1.heading_block h1 {
								font-size: 28px !important;
							}
						}
					</style>
				</head>"""+f"""

				<body style="background-color: #ffffff; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
					<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation"
						style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;" width="100%">
						<tbody>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1"
										role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #28282b; background-position: top center;"
										width="100%">
										<tbody>
											<tr>
												<td>
													<table align="center" border="0" cellpadding="0" cellspacing="0"
														class="row-content stack" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #28282b; color: #000000; width: 900px;"
														width="900">
														<tbody>
															<tr>
																<td class="column column-1"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
																	width="100%">
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="heading_block block-1" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="width:100%;text-align:center;padding-top:15px;padding-right:30px;padding-left:30px;">
																				<h1
																					style="margin: 0; color: #555555; font-size: 23px; font-family: Nunito, Arial, Helvetica Neue, Helvetica, sans-serif; line-height: 120%; text-align: left; direction: ltr; font-weight: 700; letter-spacing: normal; margin-top: 0; margin-bottom: 0;">
																					<span class="tinyMce-placeholder">MILI</span></h1>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="text_block block-2" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:10px;">
																				<div style="font-family: Arial, sans-serif">
																					<div class=""
																						style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #dfdedc; line-height: 1.2; font-family: Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;">
																						<p
																							style="margin: 0; font-size: 12px; text-align: justify; mso-line-height-alt: 14.399999999999999px;">
																							<span style="font-size:14px;"><strong>We
																									have detected suspicious login
																									activity on your account from a new
																									device. Was this you
																									? </strong></span></p>
																					</div>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="paragraph_block block-3" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-top:5px;padding-right:30px;padding-bottom:5px;padding-left:30px;">
																				<div
																					style="color:#ffffff;font-size:10px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:left;direction:ltr;letter-spacing:0px;mso-line-height-alt:12px;">
																					<p style="margin: 0;"><strong>New Login</strong></p>
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
																				style="padding-top:5px;padding-right:50px;padding-bottom:5px;padding-left:50px;">
																				<div
																					style="color:#ffffff;font-size:10px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:left;direction:ltr;letter-spacing:0px;mso-line-height-alt:12px;">
																					<p style="margin: 0;"><strong>Location *     {location}
																						</strong></p>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="paragraph_block block-5" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-right:50px;padding-bottom:5px;padding-left:50px;">
																				<div
																					style="color:#ffffff;font-size:10px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:left;direction:ltr;letter-spacing:0px;mso-line-height-alt:12px;">
																					<p style="margin: 0;"><strong>Device           {device}
																						</strong></p>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="3" cellspacing="0"
																		class="paragraph_block block-6" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad">
																				<div
																					style="color:#808080;font-size:10px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:12px;">
																					<p style="margin: 0;">*Location is approximate based
																						on the login's IP address. </p>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="paragraph_block block-7" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-top:10px;padding-right:30px;padding-bottom:10px;padding-left:30px;">
																				<div
																					style="color:#ffffff;font-size:10px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:left;direction:ltr;letter-spacing:0px;mso-line-height-alt:12px;">
																					<p style="margin: 0; margin-bottom: 16px;">If you
																						have recently attempted to log in to your
																						account from an unfamiliar device, please ignore
																						this mail.</p>
																					<p style="margin: 0;">If you did not authorize the
																						recent login attempt, please follow the steps
																						below to protect your account.</p>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="list_block block-8" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-right:40px;padding-left:40px;">
																				<ul start="1"
																					style="margin: 0; padding: 0; margin-left: 20px; list-style-type: revert; color: #ffffff; font-size: 10px; font-family: Nunito, Arial, Helvetica Neue, Helvetica, sans-serif; font-weight: 400; line-height: 120%; text-align: left; direction: ltr; letter-spacing: 0px;">
																					<li style="margin-bottom: 0px;"><span
																							style="color: #4dd29d;">Change your
																							password.</span> You'll be logged out of all
																						your active Twitter sessions except the one
																						you're using at this time.</li>
																					<li><span style="color: #4dd29d;">Check your account
																							activity</span>.</li>
																				</ul>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="paragraph_block block-10" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-top:55px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
																				<div
																					style="color:#ffffff;font-size:10px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:12px;">
																					<p style="margin: 0;"><a href="#" rel="noopener"
																							style="text-decoration: underline; color: #1ea08b;"
																							target="_blank">Help</a> | <span
																							style="color: #d457bb;"><a href="#"
																								rel="noopener"
																								style="text-decoration: underline; color: #1ea08b;"
																								target="_blank">Security tips</a></span>
																					</p>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="paragraph_block block-11" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-top:5px;padding-right:5px;padding-left:5px;">
																				<div
																					style="color:#808080;font-size:10px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:12px;">
																					<p style="margin: 0;">From</p>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="paragraph_block block-12" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-right:10px;padding-bottom:10px;padding-left:10px;">
																				<div
																					style="color:#000000;font-size:10px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:12px;">
																					<p style="margin: 0;"><strong><span
																								style="color: #00a5ff;">M<span
																									style="color: #ff0038;">i<span
																										style="color: #f6ff00;">l<span
																											style="color: #23d435;">i</span></span></span></span></strong>
																					</p>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="paragraph_block block-13" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-top:5px;padding-right:5px;padding-bottom:45px;padding-left:5px;">
																				<div
																					style="color:#808080;font-size:10px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:12px;">
																					<p style="margin: 0;">We sent this email to
																						{receiver_email}</p>
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
					</table>
				</body>

				</html>
				"""

            part = MIMEText(html, "html")
            msg.attach(part)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, msg.as_string()
                )
        except:
            messagebox.showerror("Mili", "Connection error\nTry Again")

    def forgetPasswordOTP(self):
            try:
                sender_email = self.data.get("sender")
                receiver_email = self.data.get("receiver")
                password = self.data.get("password")
                otp = self.data.get("otp")

                msg = MIMEMultipart("alternative")
                msg["Subject"] = f"{otp} to Reset Your Password"
                msg["From"] = sender_email
                msg["To"] = receiver_email
                html = """\
			<!DOCTYPE html>

			<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">

			<head>
				<title></title>
				<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
				<meta content="width=device-width, initial-scale=1.0" name="viewport" />

				<link href="https://fonts.googleapis.com/css?family=Nunito" rel="stylesheet" type="text/css" />
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

					@media (max-width:760px) {
						.desktop_hide table.icons-inner {
							display: inline-block !important;
						}

						.icons-inner {
							text-align: center;
						}

						.icons-inner td {
							margin: 0 auto;
						}

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

						.row-1 .column-1 .block-2.heading_block h1 {
							font-size: 27px !important;
						}
					}
				</style>
			</head>""" + f"""

				<body style="background-color: #ffffff; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
					<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation"
						style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;" width="100%">
						<tbody>
							<tr>
								<td>
									<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1"
										role="presentation"
										style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #28282b; background-position: top center;"
										width="100%">
										<tbody>
											<tr>
												<td>
													<table align="center" border="0" cellpadding="0" cellspacing="0"
														class="row-content stack" role="presentation"
														style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #28282b; color: #000000; width: 740px;"
														width="740">
														<tbody>
															<tr>
																<td class="column column-1"
																	style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
																	width="100%">
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="heading_block block-2" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="width:100%;text-align:center;padding-left:25px;padding-top:23px;">
																				<h1
																					style="margin: 0; color: #555555; font-size: 27px; font-family: Nunito, Arial, Helvetica Neue, Helvetica, sans-serif; line-height: 120%; text-align: left; direction: ltr; font-weight: 700; letter-spacing: normal; margin-top: 0; margin-bottom: 0;">
																					<span class="tinyMce-placeholder">MILI</span></h1>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="text_block block-3" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:10px;">
																				<div style="font-family: sans-serif">
																					<div class=""
																						style="font-size: 12px; font-family: Nunito, Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #dfdedc; line-height: 1.2;">
																						<p
																							style="margin: 0; text-align: justify; mso-line-height-alt: 14.399999999999999px;">
																							<strong>Hi,</strong></p>
																						<p
																							style="margin: 0; text-align: justify; mso-line-height-alt: 14.399999999999999px;">
																							<strong>As requested, we have sent you a One-Time Password (OTP) to reset your password. If it was
																								you, enter this confirmation code in the
																								app to reset your password:</strong></p>
																						<p
																							style="margin: 0; font-size: 12px; mso-line-height-alt: 14.399999999999999px;">
																							 </p>
																					</div>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="5" cellspacing="0"
																		class="heading_block block-4" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																		width="100%">
																		<tr>
																			<td class="pad">
																				<h1
																					style="margin: 0; color: #555555; font-size: 30px; font-family: Nunito, Arial, Helvetica Neue, Helvetica, sans-serif; line-height: 120%; text-align: center; direction: ltr; font-weight: 700; letter-spacing: normal; margin-top: 0; margin-bottom: 0;">
																					<span class="tinyMce-placeholder">{otp}</span></h1>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="paragraph_block block-5" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad"
																				style="padding-top:10px;padding-right:30px;padding-bottom:10px;padding-left:25px;">
																				<div
																					style="color:#ffffff;font-size:11px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:700;line-height:120%;text-align:justify;direction:ltr;letter-spacing:0px;mso-line-height-alt:13.2px;">
																					<p style="margin: 0;">Please note that this OTP will
																						only be valid for a limited period, so we kindly
																						request you to use it promptly to avoid any
																						inconvenience. Do not disclose OTP. If not done
																						by you, report on <a
																							href="mailto:yourvirtualmiliassistant@gmail.com?subject=Email%20regarding%20%20about%20Unauthorized%20Access%20Attempts"
																							rel="noopener"
																							style="text-decoration: underline; color: #1ea08b;"
																							target="_blank"
																							title="yourvirtualmiliassistant@gmail.com">yourvirtualmiliassistant@gmail.com</a> 
																						as FRAUD. We solicit your continued patronage to
																						our service.</p>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="2" cellspacing="0"
																		class="paragraph_block block-6" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad">
																				<div
																					style="color:#555555;font-size:9px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:10.799999999999999px;">
																					<p style="margin: 0;">from<span
																							style="color: #00a5ff;"></span></p>
																				</div>
																			</td>
																		</tr>
																	</table>
																	<table border="0" cellpadding="0" cellspacing="0"
																		class="paragraph_block block-7" role="presentation"
																		style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																		width="100%">
																		<tr>
																			<td class="pad" style="padding-bottom:35px;">
																				<div
																					style="color:#000000;font-size:11px;font-family:Nunito, Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:13.2px;">
																					<p style="margin: 0;"><strong><span
																								style="color: #00a5ff;">M<span
																									style="color: #ff0038;">i<span
																										style="color: #f6ff00;">l<span
																											style="color: #23d435;">i</span></span></span></span></strong>
																					</p>
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
					</table>
				</body>
				</html>
				"""
                part = MIMEText(html, "html")
                msg.attach(part)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(
                        sender_email, receiver_email, msg.as_string()
                    )
            except Exception as e:
                messagebox.showerror("Mili", "Connection error\nTry Again")