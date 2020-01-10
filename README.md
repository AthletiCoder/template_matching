# Template Matching
### Used to find if a large input image contains smaller template images

## Requirements
* python version 3.6.8 
* Install the requirements of the project using the command `pip3 install -r requirements.txt` at root level of project
* Put all the template images in a folder in root level

## Usage

### For Command line interface
`python3 template_matching.py -t <TEMPLATES_DIR> -i <INPUT_PATH> -v`

### For Graphical user interface
`python3 main.py`

## Results
A csv file showing the results will be created

| Input image   |  Template  | Found |  Correlation |  Scale |
|:-------------:|:----------:|:-----:|:------------:|:------:|
|large_image.tif| small2.jpg | FALSE | 0.12779242   | 0.7143 |
|large_image.tif| small1.jpg | TRUE  | 0.06805718   | 0.8333 |

A folder with best found matches of the templates is shown as follows
![alt text](https://github.com/AthletiCoder/template_matching/blob/gui/sample_result.jpg "Logo Title Text 1")
