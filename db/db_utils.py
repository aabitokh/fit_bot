from models.db_models import Training_session
from db.main_db import Session
from logger.logger import get_logger
from models.training import Training

logger = get_logger()

def add_trainig(tr = Training):

    logger.debug('открывается сессия для внесения тренировки')
    session = Session()

    for mg in tr.muscle_groups:
        for exc in list(tr.data['muscle_group'][mg].keys()):
            ts = Training_session(time_key=tr.start_training, 
                          muscle_group=mg, 
                          exercise = exc, 
                          tonnage = tr.tonnage[exc])
            session.add(ts)
    
    session.flush()
    session.commit()
    
    logger.info('тренировка добавлена')
    session.close()
