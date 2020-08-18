# Installation
### Dependencies
 - opencv-python (>=4.3.0.36)
 - numpy (>= 1.19.1)
 - pandas (>= 1.1.0)
# Binary Image
Binary image.

### Parameters:
- __image__ : numpy.ndarray, image type is gray, default : None
- __way__ : string, the way of how to binary, default : otsu, could be : otsu, threshold.

### Returns:
- __image__ : numpy.ndarray, image type is gray, default : None

### Methods:
- __fit__()

### Examples:

```python
import cv2 as cv
from detect_exposure import DetectExposure

img = cv.imread(path, cv.IMREAD_GRAYSCALE)#read image
binaryImage = BinaryImage(img) 
binary_img = binaryImage.fit()
```