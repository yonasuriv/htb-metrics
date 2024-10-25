import imgkit
from PIL import Image

def html_to_png_with_transparency(html_file, output_png):
    # Step 1: Convert HTML to PNG using imgkit
    options = {
        'enable-local-file-access': '',             # Allow local file access if necessary
        'transparent': ''                           # Optional, but might not work with wkhtmltoimage, so we'll do post-processing
    }
    
    imgkit.from_file(html_file, output_png, options=options)

    # Step 2: Open the PNG image and process the transparency
    img = Image.open(output_png)
    img = img.convert("RGBA")  # Ensure the image is in RGBA mode

    # Create a new data array for the modified image
    new_data = []
    
    for item in img.getdata():
        # Check if the pixel is white (R=255, G=255, B=255)
        if item[:3] == (255, 255, 255):             # Pure white
            new_data.append((255, 255, 255, 0))     # Make it fully transparent
        else:
            new_data.append(item)                   # Keep original pixels

    # Apply the new data to the image and save it
    img.putdata(new_data)
    img.save(output_png, "PNG")
    print(f"Converted {html_file} to PNG with transparent background saved as {output_png}")

# Example usage
template = 'badge-default'
html_file = '../assets/templates/{template}.html'   # Path to the HTML file
output_png = '{template}.png'                       # Path to the output PNG file
html_to_png_with_transparency(html_file, output_png)
