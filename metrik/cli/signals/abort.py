import asyncio
import os
import signal
from metrik.logging import MetrikLogger
from multiprocessing import current_process, active_children

def handle_loop_stop(
    signame,
    logger: MetrikLogger,
):
        try:
      
            child_processes = active_children()
            for child in child_processes:
                child.kill()
                
            process = current_process()
            if process:
                try:
                    process.kill()
                
                except Exception:
                    pass

        except BrokenPipeError:
            logger.console.sync.critical('\n\nAborted.\n')   

        except RuntimeError:
            logger.console.sync.critical('\n\nAborted.\n')

        if len(child_processes) < 1:
            logger.console.sync.critical('\n\nAborted.\n')   
            os._exit(1)

def add_abort_handler(
    loop: asyncio.AbstractEventLoop, 
    logger: MetrikLogger
):
    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(
            getattr(signal, signame),
            lambda signame=signame: handle_loop_stop(
                signame, 
                logger
            )
        )