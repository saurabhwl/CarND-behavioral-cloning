# CarND-behavioral-cloning

##Overview
I follow the following steps for the project  
  1. load the driving log in memory  
  2. visualize the images and steering angle  
  3. preprocessing  
  4. build the model  
  5. feed the images/angle to model in batches using generator  
  6. fit the model   
  7. test the model  
  8. save the model  
  9. drive on track using the saved model  


##Preprocessing
Information such as how the dataset was generated and examples of images from the dataset should be included.
Preprocessing image is the most critical part. I took the following steps to ensure that I am feeding the quality data to model so it will train properly. In the captured images, there are a lot of background noise, trees and mountains  etc. They are not useful in training. They do create distraction in the model. So it is very important to crop the image to right size to only feed the portion of image that are important for model to learn. 

Second, data we collected from training track has images with steering on right. It is skew towards the steering towards right. To tackle that, I flip the images so that the data is more balanced. third, we have images from left, right and center camera along with steering angles. We need to adjust steering angle from left and right camera to get the correct input to our model. 

##Model architecture
provides sufficient details of the characteristics and qualities of the architecture, such as the type of model used, the number of layers, the size of each layer. Visualizations emphasizing particular qualities of the architecture are encouraged.


##Training dataset 
I am using the training datasets provided by Udacity. I found it more accurate than the data I collected. The part of that training using keyboards does not produce the quality datasets. 

##Training process

##Conclusion

