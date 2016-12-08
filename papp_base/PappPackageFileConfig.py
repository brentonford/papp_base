"""
 Copyright Synerty Pty Ltd 2013

 This software is proprietary, you are not free to copy
 or redistribute this code in any format.

 All rights to this software are reserved by 
 Synerty Pty Ltd

 :Website: http://www.synerty.com
 :Support: support@synerty.com

"""

import logging
import os

from jsoncfg.functions import save_config, ConfigWithWrapper

logger = logging.getLogger(__name__)


class PappPackageFileConfig(object):
    """
    This class helps with accessing the config for the papp_package.json
    """

    def __init__(self, pappRootDir: str):
        """
        Constructor

        :param pappRootDir: The root directory of this package, where papp_package.json
        lives.
        """
        self._pappRoot = pappRootDir
        if not os.path.isdir(self._pappRoot): raise NotADirectoryError(self._pappRoot)

        self._configFilePath = os.path.join(pappRootDir, 'papp_package.json')

        if not os.path.isfile(self._configFilePath):
            assert (not os.path.exists(self._configFilePath))
            with open(self._configFilePath, 'w') as fobj:
                fobj.write('{}')

        self._cfg = ConfigWithWrapper(self._configFilePath)

    def _save(self):
        """ Save

        Saves the config back to the json file.
        The output will be standard json.
        """
        save_config(self._configFilePath, self._cfg)

    @property
    def config(self) -> ConfigWithWrapper:
        """ Config

        :return: The jsoncfg config object, for accessing and saving the config.
        """
        return self._cfg
