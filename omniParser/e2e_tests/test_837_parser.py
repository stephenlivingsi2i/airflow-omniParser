from omniparser.parser import OmniParser


parser = OmniParser("837")
parser.transform("data/837/837_original.txt", "outputs/837/837_original.json")