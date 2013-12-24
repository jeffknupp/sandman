"""Test that foreign keys with non-trivial keys are properly ignored."""
from sandman.model import register, activate, Model

class JobSchedule(Model):
    """JobSchedule table"""
    __tablename__ = 'job_schedule'

class DataSources(Model):
    """DataSources table"""
    __tablename__ = 'data_sources'

register((JobSchedule, DataSources))
activate(admin=False)
