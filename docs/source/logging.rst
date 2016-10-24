================================================================================
How to log pyexcel
================================================================================

When developing source plugins, it becomes necessary to have log trace available.
It helps find out what goes wrong quickly.

The basic step would be to set up logging before pyexcel import statement.
    
.. code-block:: python

    import logging
    import logging.config
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
     
    import pyexcel 
    
And if you would use a complex configuration, you can use the following code.

.. code-block:: python

    import logging
    import logging.config
    logging.config.fileConfig('log.conf')
     
    import pyexcel 

And then save the following content as log.conf in your directory::

    [loggers]
    keys=root, sources, renderers
    
    [handlers]
    keys=consoleHandler
    
    [formatters]
    keys=custom
    
    [logger_root]
    level=INFO
    handlers=consoleHandler
    
    [logger_sources]
    level=DEBUG
    handlers=consoleHandler
    qualname=pyexcel.sources.factory
    propagate=0
    
    [logger_renderers]
    level=DEBUG
    handlers=consoleHandler
    qualname=pyexcel.renderers.factory
    propagate=0
    
    [handler_consoleHandler]
    class=StreamHandler
    level=DEBUG
    formatter=custom
    args=(sys.stdout,)
    
    [formatter_custom]
    format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
    datefmt=
