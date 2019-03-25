from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from database import Base

from datetime import datetime
from sqlalchemy.orm import relationship


STATUS_MAP = {
    0: 'submitted',
    1: 'in-progress',
    2: 'completed'
}

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    submitted = Column(String)

    network = Column(String)
    layer = Column(String)
    channel = Column(String)

    status = Column(Integer)
    visualization = relationship('Visualization', back_populates='produced_by')

    def __init__(self, network, layer, channel='', submitted=None):
        self.network = network
        self.layer = layer
        self.channel = channel

        if not submitted:
            submitted = datetime.now().strftime('%Y%m%d-%H%M%S')

        self.submitted = submitted
        self.status = 0 # initially the job is submitted

    def __repr__(self):
        return f'<Job {self.submitted}, {self.network}, {self.layer}, {self.status}>'


class Visualization(Base):
    __tablename__ = 'visualizations'
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    produced_by = relationship('Job', back_populates='visualization')
    results = relationship('VisualizationResult',
                           back_populates='visualization')

    def __init__(self, job):
        self.produced_by = job

    def __repr__(self):
        return f'<Visualization {self.produced_by}>'


class VisualizationResult(Base):
    __tablename__ = 'visualization_results'
    id = Column(Integer, primary_key=True)
    img_name = Column(String)
    created_at = Column(String)
    vis_id = Column(Integer, ForeignKey('visualizations.id'))
    visualization = relationship('Visualization', back_populates='results')


    def __init__(self, img_name, vis):
        self.created_at = datetime.now().strftime('%Y%m%d-%H%M%S')
        self.img_name = img_name
        self.visualization = vis


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)
