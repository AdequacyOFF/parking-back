import json
import subprocess


def get_car_number(image_path: str) -> str:
    command = ["openalpr_64\\alpr", "-j", image_path]

    result = subprocess.run(command, capture_output=True, text=True).stdout

    if result == '':
        return "0"

    outputs = json.loads(result)['results'][0]['candidates']

    plates = [plate['plate'] for plate in outputs]

    prediction = plates[0]

    for plate in plates:
        if len(plate) == 6:
            prediction = plate
            break

    return prediction
