import base64

def file_to_base64(file_path):
    with open(file_path, "rb") as file:
        # Read the file contents
        file_contents = file.read()
        
        # Encode the file contents as Base64
        base64_encoded = base64.b64encode(file_contents)
        
        return base64_encoded.decode("utf-8")  # Convert bytes to string


file_path = "getassets.py"
filecontent = '''
def get_ding_WAVbase64():
    return """{}"""


def get_icon_data():
    return """{}"""

'''.format(file_to_base64("assets/Alarm_Ringtone.wav"), file_to_base64("assets/pomodoro.png"))

with open(file_path, "w") as output_file:
            output_file.write(filecontent) 