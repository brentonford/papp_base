from twisted.trial import unittest

from peek.core.model.ModelUtil import trace
from peek.core.orm import getNovaOrmSession
from peek.core.orm.ModelSet import ModelNode


class ModelUtilTest(unittest.TestCase):

    def testTraceHb9(self):
        session = getNovaOrmSession()
        hb9Node = session.query(ModelNode).filter(ModelNode.id == 1010114).one()
        print trace(hb9Node, depth=8)