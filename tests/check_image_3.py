import fast_colorthief

image_path = 'h663_tn.jpg'

dominant_color = fast_colorthief.get_dominant_color(image_path)
color_palette = fast_colorthief.get_palette(image_path)
