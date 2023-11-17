import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import numpy as np

# Function to convert RGB to Hex


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

# Function to extract color from an solid color image


def extract_color(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    # Since it's a solid color, take the mid pixel
    color = np.array(image)[50][50]
    return rgb_to_hex(color)


# Load the CSV file
df = pd.read_csv('swatches.csv')

# Add a new column for hex colors
df['Hex Color'] = df['Image Link'].apply(extract_color)

# Save the updated DataFrame to a new CSV file
df.to_csv('updated_colors.csv', index=False)
