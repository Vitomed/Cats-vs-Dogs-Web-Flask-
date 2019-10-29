import numpy
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing import image
from tensorflow.python.keras.applications.vgg16 import preprocess_input


class mymodel:

    def __init__(self, type, file):
        self.new_model = load_model(type)
        self.file_name = file
        self.img = image.load_img(self.file_name, target_size=(150, 150))
        self.x = image.img_to_array(self.img)
        self.x = numpy.expand_dims(self.x, axis=0)
        self.x = preprocess_input(self.x)
        self.pred = self.new_model.predict(self.x)
        self.number = int(self.pred[0][0])

    def __repr__(self):
        if self.number == 1:
            return "Dog"
        else:
            return "Cat"

type = 'net/binary.h5'
file = 'dog.jpg'
dog = mymodel(type, file)
print(dog)
