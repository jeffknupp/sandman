from sandman.model import register, activate, Model

class JobSchedule(Model):
    __tablename__ = 'job_schedule'

class DataSources(Model):
    __tablename__ = 'data_sources'

register((JobSchedule, DataSources))
activate(admin=False)
