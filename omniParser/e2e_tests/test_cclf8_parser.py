from omniParser.omniparser.parser import OmniParser


parser = OmniParser("CCLF_CCLF8")
parser.transform("data/cclf/cclf8.txt", "outputs/cclf/cclf8.json")

# S3 example
# parser.transform("s3://sureshn-hec-landing-bucket/cclf8.txt", "s3://sureshn-hec-landing-bucket/cclf8.json")
