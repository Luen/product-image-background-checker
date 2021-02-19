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
- Move functions to a separate helper file for easy importing into a custom script
- Then create a test script for both local image file and URL
