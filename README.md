# Finding Missing people through AI

Machine Learning project to find people from an Image.

Lets Image a senario
1. A child goes missing.
2. The child's parents will go to police for FIR.
3. The police will collect child's photo and will forward to near stations and will start looking for him/her.
This is the conventional method and isn't it too much work to do? And for how many people police can apply this method?

So, we will apply AI here.
1. Child's photo will be scanned and unique key points of his face will be generated.
2. These key points will be stored in DB.
3. Now, imagine next day this child is begging on road in a complete different state.
4. A person passing by clicks his picture.
5. Unique points for that picture clicked will be generated.
6. Both the points generated will be compared.
7. The last location of the matched points will be shared. In this manner police will come to know where the child was seen last.



Built with the help of [dlib's](http://dlib.net/) state-of-the-art face recognition built with deep learning.
The model has an accuracy of 99.38% on the [Labeled Faces in the Wild](http://vis-www.cs.umass.edu/lfw/) benchmark.

## Dependencies:

- Python 3.x
- Numpy
- Scipy
- [Scikit-learn](http://scikit-learn.org/stable/install.html)
- [dlib](http://dlib.net/)

    

## Vote of Thanks
- Thanks to [Davis King](https://github.com/davisking) for creating dlib and for providing the trained facial feature
  detection and face encoding models used in this project.
