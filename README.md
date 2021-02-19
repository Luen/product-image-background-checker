# Check background of product photos
A python script for personal-use that processes a csv of image URLs and outputs several test results to csv. Checks and outputs:
- file extension
- dominant colour: (R,G,B)
- dominant colour: web colour name (if applicable, else convert to RBG to basic text)
- dominant colour: closest web colour name
- dominant shade: (black or white)
- top left pixel: (R,G,B)
- top left pixel: web colour name (if applicable, else convert to RBG to basic text)
- image: height
- image: width
- is transparent

# Install
- Install [Python](https://www.python.org/downloads/)
- Install packages / modules (will show up in errors)
- Edit the script/csv file

# Run
`python check_images.py`

# To Do
- Move functions to a separate helper file for easy importing into a custom script for future use.
- Then create a test script for both local image files and URLs.
- Get a sample region (20 pixel in from the top and 20 pixel in from the left and then select a 20 x 20 pixel sample) and check for dominant colour. This method would avoid the Shopify plugin that squares images and adds white on the image sides. E.g., a black image that's not square get white added to the sides to make it a square image.
- Add check to see if image is squared. If not squared, the image may not be tainted (by the Shopify squaring plugin) and then can maybe use the top left pixel accurately...
