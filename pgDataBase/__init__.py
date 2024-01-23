# -*- encoding:utf-8 -*-

import datetime
import psycopg2
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String, Integer, Boolean, Text, DATE


Base = declarative_base()