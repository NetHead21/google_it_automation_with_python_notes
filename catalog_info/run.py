#! /usr/bin/env python3

# sourcery skip: avoid-builtin-shadow, raise-specific-error
import os
import requests
import re

# desc_path = os.path.expanduser('~') + '/supplier-data/descriptions/'
# image_path = os.path.expanduser('~') + '/supplier-data/images/'
desc_path = "supplier-data/descriptions/"
image_path = "supplier-data/images/"

text_files = sorted(os.listdir(desc_path))
jpeg_images = sorted(
    [image_name for image_name in os.listdir(image_path) if ".jpeg" in image_name]
)

list_content = []
image_counter = 0

format = ["name", "weight", "description"]

for file in text_files:
    """
    Note that all files are written in the following format, with each piece of information on its own line:
    * name
    * weight (in lbs)
    * description
    """
    with open(desc_path + file, "r") as f:
        contents = f.read().split("\n")[:3]
        # print(contents)

        """
        The weight field is defined as an integer field. 
        So when you process the weight information of the fruit from the .txt file, you need to convert it into an integer. 
        For example if the weight is "500 lbs", you need to drop "lbs" and convert "500" to an integer.
        """
        contents[1] = int(
            (re.search(r"\d+", contents[1])).group()
        )  # The weight field is defined as an integer field.
        data = {format[counter]: content for counter, content in enumerate(contents)}
        """
        The image_name field will allow the system to find the image associated with the fruit. 
        Don't forget to add all fields, including the image_name!
        """
        data["image_name"] = jpeg_images[image_counter]

        list_content.append(data)
        image_counter += 1

"""
 The final JSON object should be similar to:

{
    "name": "Watermelon", 
    "weight": 500, 
    "description": "Watermelon is good for relieving heat, eliminating annoyance and quenching thirst. 
                    It contains a lot of water, which is good for relieving the symptoms of acute fever immediately. 
                    The sugar and salt contained in watermelon can diuretic and eliminate kidney inflammation. 
                    Watermelon also contains substances that can lower blood pressure.", 
    "image_name": "010.jpeg"
}
"""

for item in list_content:
    resp = requests.post("http://127.0.0.1:80/fruits/", json=item)
    if resp.status_code != 201:
        raise Exception(f"POST error status={resp.status_code}")
    print(f'Created feedback ID: {resp.json()["id"]}')
