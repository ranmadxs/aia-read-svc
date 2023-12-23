from argparse import ONE_OR_MORE, ArgumentParser
from . import __version__
from .yahooMailSvc import YahooMail
from .read_svc import ReadSvc
import os
from dotenv import load_dotenv
load_dotenv()

def run():
    """
    entry point
    """
    parser = ArgumentParser(prog="daemon", description="XD")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    #parser.add_argument(dest="users", nargs=ONE_OR_MORE, type="User", help="your name")
    #args = parser.parse_args()
    print ("XDDDDD GET MAILS DAEMON")
    readSvc = ReadSvc(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], __version__)    
    readSvc.readDaemon() 

    #yahooMail = YahooMail(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], __version__)
    #yahooMail.mailDaemon()