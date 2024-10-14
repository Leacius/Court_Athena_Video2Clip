import yaml
import argparse
from vidoe2clips import Clips

if __name__ == "__main__":

    parser = argparse.ArgumentParser( description="PyTorch implementation of Temporal Segment Networks" )
    ### ============================ save config ============================ ###
    parser.add_argument("--save-root", type=str, default="./processed_data/")
    
    args = parser.parse_args()
    args = vars(args)

    # open config file
    with open("./configs/process.yaml", "r") as f:
        args.update(yaml.safe_load(f))
    args = argparse.Namespace(**args)

    container = Clips(args)
    container.Run(args.eventType)