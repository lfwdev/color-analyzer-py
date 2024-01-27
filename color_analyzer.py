import time
import numpy as np
import colorsys
from colorthief import ColorThief
from sklearn.cluster import KMeans

# Specify the path to your image file
image_path = 'E:\\Coding\\color-analizer\\storage\\palette sampler 2.jpg'

# Create a ColorThief object
color_thief = ColorThief(image_path)

# Get the dominant color
dominant_color = color_thief.get_color(quality=1)

# Get a color palette
palette = color_thief.get_palette(color_count=255)

def rgb_to_hex(rgb):
    # """Convert RGB color code to hex color code."""
    hex_color = "#{:02x}{:02x}{:02x}".format(*rgb)
    return hex_color

def rgb_to_hsv(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    return colorsys.rgb_to_hsv(r, g, b)

def count_colors(palette):
    color_counter = {}
    
    for c in palette:
        color_hex = ''.join(format(c, '02x') for c in c)
        if color_hex not in color_counter:
            color_counter[color_hex] = 1
        else:
            color_counter[color_hex] += 1

    print(color_counter)
    return color_counter

def group_similar_colors(palette):
    # Use k-means clustering to group colors
    kmeans = KMeans(n_clusters=10)  # You can adjust the number of clusters
    labels = kmeans.fit_predict(palette)

    color_groups = []
    for i, label in enumerate(labels):
        color = palette[i]

        added = False
        for group in color_groups:
            if label == group['label']:
                group['colors'].append(color)
                added = True
                break
        if not added:
            color_groups.append({'label': label, 'colors': [color]})

    return color_groups

def generate_html_from_palette(color_groups, color_counter):
    # Start the HTML code
    html_code = "<!DOCTYPE html>\n<html>"
    html_code += f"\n<head>\n<title>Color Analyzer | {str(image_path)}</title>"
    html_code += "\n<style> html { background-color: #333; color: #FFF; } </style>"
    html_code += "\n</head>\n<body>\n"
    # Initialize a dictionary to store color counts
    color_counts = {}

    # Iterate through the color groups
    for group in color_groups:
        group_colors = group['colors']
        
        # Sort group colors by the first color's hue
        group_colors = sorted(group_colors, key=lambda x: rgb_to_hsv(x)[0])

        # Generate HTML code for each color group
        for rgb_color in group_colors:

            # Increment color count or initialize if not present
            color_hex = ''.join(format(c, '02x') for c in rgb_color)
            if color_hex not in color_counts:
                color_counts[color_hex] = 1
            else:
                color_counts[color_hex] += 1

            color_div = f"<div style='display: flex; align-items: center;'>\n"
            color_div += f"  <div style='width: 16px; height: 32px; background-color: rgb{rgb_color};'></div>\n"
            color_div += f"  <div style='width: 16px; height: 32px; background-color: {rgb_to_hex(rgb_color)};'></div>\n"
            color_div += f"  <div style='margin-left: 8px;'> {rgb_to_hex(rgb_color)} | rgb{rgb_color} ({color_counter[color_hex]})</div>\n"
            color_div += f"</div>\n"

            # Append the color div to the HTML code if it's the first occurrence
            if color_counts[color_hex] == 1:
                html_code += color_div

        # Add a separator between color groups
        html_code += "<hr>\n"

    # End the HTML code
    html_code += "</body>\n</html>"

    return html_code

# run
color_counter = count_colors(palette)
color_groups = group_similar_colors(palette)
html_output = generate_html_from_palette(color_groups, color_counter)

# Save the HTML code to a file
with open('color_palette_result' + str(int(time.time())) + '.html', 'w') as html_file:
    html_file.write(html_output)
