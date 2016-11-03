""" 
 *  Copyright Synerty Pty Ltd 2016
 *
 *  This software is proprietary, you are not free to copy
 *  or redistribute this code in any format.
 *
 *  All rights to this software are reserved by 
 *  Synerty Pty Ltd
 *
"""
import logging

from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.sql.schema import Index

from papp_noop.storage.DeclarativeBase import DeclarativeBase
from rapui.vortex.Tuple import Tuple, addTupleType, TupleField

logger = logging.getLogger(__name__)


@addTupleType
class NoopTable(Tuple, DeclarativeBase):
    """ NoopTable

    This table doesn't do anything

    """
    __tupleType__ = 'papp_noop.NoopTable'
    __tablename__ = 'NoopTable'

    id = Column(Integer, primary_key=True)
    string1 = Column(String)

    nonDbField = TupleField()

    __table_args__ = (
        Index("idx_NoopTable_unique_index", id, string1,
              unique=True),
    )
