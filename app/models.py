from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Issue(Base): #extends Base model of sql alchemy
    __tablename__="issues"

    id = Column(Integer, primary_key=True, nullable=False)
    issue= Column(String, nullable=False)
    challenge= Column(String, nullable=False)
    sector=Column(String, nullable=False)
    location=Column(String, nullable=False)
    published= Column(Boolean, server_default='True', nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'), nullable=False)
    citizen_id = Column(Integer, ForeignKey("citizens.id", ondelete="CASCADE"), nullable=False)
    
    citizen = relationship("Citizen")

class Citizen(Base): #extends Base model of sql alchemy
    __tablename__="citizens"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    email= Column(String, nullable=False, unique=True)
    password= Column(String, nullable=False)
    location=Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'), nullable=False)

class DecisionMaker(Base): 
    __tablename__="decision_makers"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    email= Column(String, nullable=False, unique=True)
    password= Column(String, nullable=False)
    organization=Column(String, nullable=False)
    authority=Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'), nullable=False)

class Focus(Base): #extends Base model of sql alchemy
    __tablename__="focus_issues"

    id = Column(Integer, primary_key=True, nullable=False)
    issue_id=Column(Integer, ForeignKey("issues.id", ondelete="CASCADE"), nullable=False)
    decisionmaker_id = Column(Integer, ForeignKey("decision_makers.id", ondelete="CASCADE"), nullable=False)
    status= Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'), nullable=False)
    published= Column(Boolean, server_default='True', nullable=False)

    decisionmaker = relationship("DecisionMaker")
    issue = relationship("Issue")