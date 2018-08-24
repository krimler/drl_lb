import logging
logger = None
HDLR = None
FORMATTER = None
if(None == logger):
    logger = logging.getLogger('reinf_load_balancer')
    HDLR = logging.FileHandler('/Users/madgaikw/sonal/reinf_load_balancer.log')
    FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    HDLR.setFormatter(FORMATTER)
    logger.addHandler(HDLR) 
    logger.setLevel(logging.WARNING)
    logger.critical('STARTED------------------>')
#logger.error('We have a problem')
#logger.info('While this is just chatty')


