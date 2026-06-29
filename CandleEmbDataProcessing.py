# import required modules
import os
import glob
import random
import torch
from torch.utils.data import Dataset, DataLoader, random_split
import torchvision.io
import torchvision.transforms as transforms
from sklearn.model_selection import train_test_split




class CandleImageDataSet(
    Dataset
):
    

    def __init__(
        self,
        paths : list[str],
        image_size : tuple[int,int],
        normalize = None
    ):
        
        self.images = []
        self.paths = paths

        resize = transforms.Resize(
            size = image_size
        )

        for p in self.paths :

            image = torchvision.io.read_image(
                path = p
            )

            if image.shape[0] == 1 :
                # make image RGB
                image = image.repeat( 3 , 1 , 1)

            if image.shape[0] == 4 :

                image = image[0:3 , : , :]
            image = resize( image )
            image = image.float()/255.0


            self.images.append( image )

        self.normalize = normalize


    def __len__(
        self
    ):
        
        return len( self.images )
    
    def __getitem__(self, index):
        
        image = self.images[index]

        if self.normalize :

            image = self.normalize( image )
        
        return image, image
    
if __name__ == "__main__":

    ################
    # Cinfiguration#
    ################

    IMAGE_DIR = "./BTC"
    IMGAG_SIZE = (504, 420)
    BATCH_SIZE = 64
    NUM_WORKER = min( os.cpu_count(), 6)
    RANDOM_SEED = 42


    ####################
    #get all image path#
    ####################

    image_paths = glob.glob(
        os.path.join(
            IMAGE_DIR,
            "*.png"
        )
    )

    train_path, temp_path = train_test_split(
        image_paths, test_size = 0.7, random_state = RANDOM_SEED
    )

    validation_path, test_path = train_test_split(
        temp_path, test_size = 0.66, random_state = RANDOM_SEED
    )


    train_dataset = CandleImageDataSet(
        paths = train_path,
        image_size = IMGAG_SIZE
    )

    train_dataloader = DataLoader(
        dataset = train_dataset,
        batch_size = BATCH_SIZE,
        shuffle = True
    )


    for x,y in train_dataloader :

        print( x[0].shape ) 
        break