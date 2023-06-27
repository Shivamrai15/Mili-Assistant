from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from winsdk.windows.devices import radios
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# ------------------------------------------------------------------------------------------------------


# This funnction is used to turn on bluetooth and turn off bluetooth
# pass True to turn on bluetooth
# pass False to turn of bluetooth
# ------------------------------------------------------------------------------------------------------
async def bluetooth(value):
    all_radios = await radios.Radio.get_radios_async()
    for radio in all_radios:
        if radio.kind == radios.RadioKind.BLUETOOTH:
            if value:
                result = await radio.set_state_async(radios.RadioState.ON)
            else:
                result = await radio.set_state_async(radios.RadioState.OFF)
# ------------------------------------------------------------------------------------------------------


# This funnction is used to turn on wifi and turn off wifi
# pass True to turn on wifi
# pass False to turn of wifi
# ------------------------------------------------------------------------------------------------------
async def WIFI(turn_on):
    all_radios = await radios.Radio.get_radios_async()
    for radio in all_radios:
        if radio.kind == radios.RadioKind.WI_FI:
            if turn_on:
                result = await radio.set_state_async(radios.RadioState.ON)
            else:
                result = await radio.set_state_async(radios.RadioState.OFF)
# ------------------------------------------------------------------------------------------------------


# This function is used to increase or decrease the volume
# ------------------------------------------------------------------------------------------------------
def change_volume():
    # Get the default audio endpoint for the system
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    # Query the interface for the volume control
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Get the current volume range
    min_vol, max_vol, _ = volume.GetVolumeRange()

    # Get the current volume level
    current_vol = volume.GetMasterVolumeLevel()

    # Calculate the desired volume level (increase by 1 decibel)
    desired_vol = current_vol + 5

    # Ensure the desired volume is within the valid range
    desired_vol = max(min_vol, min(desired_vol, max_vol))

    # Set the new volume level
    volume.SetMasterVolumeLevel(desired_vol, None)
# ------------------------------------------------------------------------------------------------------

