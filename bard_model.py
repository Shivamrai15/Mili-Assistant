from encryption import Encryption
from bardapi import Bard
import os

key = Encryption(
    b"gAAAAABkpIgBUVYB8vDGw_Hm2Fjyrl828SfEjnJFw8XBiG1BYvlDNP78MtGeSDT0ejin1xR6AffRwfcH3AoUQRodyOJu9dAkwsekeNLzKDum8ux3Uk8_uGDGw1Z9-j3J2s2DVMtkl7OtnokeQdItJl1nDbXRHPeQX6ovrGiTILXtyIggNEfxxzc="
).decrypt_text()
os.environ["_BARD_API_KEY"] = key


def bardResponse(prompt: str):
    response = Bard().get_answer(prompt)
    response = str(response.get("content"))
    response = response.replace("**", '"')
    response = response.replace("*", "\U00002022")
    return response
