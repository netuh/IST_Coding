from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from coding_tool import db

association_experiment = db.Table('association_experiment', db.metadata,
                                  db.Column('pub_id', db.Integer,
                                            db.ForeignKey('publication.pub_id')),
                                  db.Column('exp_id', db.Integer,
                                            db.ForeignKey('experiment.exp_id')),
                                  )

association_guideline = db.Table('association_guideline', db.metadata,
                                 db.Column('pub_id', db.Integer,
                                           db.ForeignKey('publication.pub_id')),
                                 db.Column('guide_id', db.Integer,
                                           db.ForeignKey('guideline.guide_id')),
                                 )

association_profile = db.Table('association_profile', db.metadata,
                               db.Column('profile_id', db.Integer,
                                         db.ForeignKey('sampling_profile.profile_id')),
                               db.Column('sample_id', db.Integer,
                                         db.ForeignKey('sampling.sample_id')),
                               )

association_charac = db.Table('association_charac', db.metadata,
                              db.Column('charac_id', db.Integer,
                                        db.ForeignKey('sampling_charac.charac_id')),
                              db.Column('sample_id', db.Integer,
                                        db.ForeignKey('sampling.sample_id')),
                              )

association_task = db.Table('association_task', db.metadata,
                            db.Column('design_id', db.Integer,
                                      db.ForeignKey('experiment_design.design_id')),
                            db.Column('task_id', db.Integer,
                                      db.ForeignKey('task.task_id')),
                            )


class Publication(db.Model):
    __tablename__ = 'publication'
    pub_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.String(200), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    keywords = db.Column(db.String(200), nullable=False)
    experiments = db.relationship("Experiment", backref="pub", lazy='dynamic')

    def __repr__(self):
        return f"Publication('{self.title}', '{self.year}')"


class Guideline(db.Model):
    __tablename__ = 'guideline'
    guide_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    authors = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    referenced_by = db.relationship('Publication', secondary=association_guideline,
                                    backref=db.backref('guidelines', lazy='dynamic'))

    def __repr__(self):
        return f"Guideline('{self.title}', '{self.year}')"


class Experiment(db.Model):
    __tablename__ = 'experiment'
    exp_id = db.Column(db.Integer, primary_key=True)
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.pub_id'))
    samples = db.relationship("Sampling", backref="exp", lazy=True)
    design = db.relationship("ExperimentDesign", uselist=False,
                             back_populates="experiment")
    lab_settings = db.Column(db.Integer)
    # design_id = db.Column(db.Integer, db.ForeignKey(
    #     'experiment_design.design_id'), nullable=True)


class Sampling(db.Model):
    __tablename__ = 'sampling'
    sample_id = db.Column(db.Integer, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey('experiment.exp_id'))
    recruiting_strategy = db.Column(db.String(200))
    power_analysis = db.Column(db.Integer, default=0)
    profiles = db.relationship(
        'SamplingProfile', secondary=association_profile)
    characteristics = db.relationship(
        'SamplingCharacteristic', secondary=association_charac)

    def __repr__(self):
        return f"Sampling('{self.recruitment_type}', '{self.sample_size}')"

    def sample_classification(self):
        has_student = False
        has_professional = False
        total = 0
        classification = 0
        for a_profile in self.profiles:
            if (a_profile.profile == 'professional'):
                has_professional = True
            else:
                has_student = True
            total += a_profile.quantity
        if (has_student and has_professional):
            return 'mix', total
        elif (has_professional):
            return 'professional_only', total
        else:
            return 'student_only', total


class SamplingProfile(db.Model):
    __tablename__ = 'sampling_profile'
    profile_id = db.Column(db.Integer, primary_key=True)
    profile = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class SamplingCharacteristic(db.Model):
    __tablename__ = 'sampling_charac'
    charac_id = db.Column(db.Integer, primary_key=True)
    charac = db.Column(db.String(20), nullable=False)
    info = db.Column(db.String(100), nullable=True)


class ExperimentDesign(db.Model):
    __tablename__ = 'experiment_design'
    design_id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.exp_id'))
    experiment = db.relationship("Experiment", back_populates="design")
    factor_quantity = db.Column(db.Integer, nullable=False)
    design = db.Column(db.String(20), nullable=False)
    is_explicity_design = db.Column(db.Integer, nullable=False)
    tasks = db.relationship('Task', secondary=association_task)
    duration = db.relationship("Duration", uselist=False,
                               back_populates="parent")
    measurements = db.relationship("Measurement", uselist=False,
                                   back_populates="parent")


class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True)
    task_type = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)


class Duration(db.Model):
    __tablename__ = 'durantion'
    durantion_id = db.Column(db.Integer, primary_key=True)
    durantion_type = db.Column(db.String(4))
    amount = db.Column(db.FLOAT)
    metric = db.Column(db.String(8))
    parent_id = db.Column(db.Integer, db.ForeignKey(
        'experiment_design.design_id'))
    parent = db.relationship("ExperimentDesign", back_populates="duration")

    def classification(self):
        if self.metric.startswith('min'):
            return '>1h'
        elif self.metric.startswith('hour'):
            if self.amount < 1:
                return '>1h'
            elif 1 <= self.amount < 2:
                return '1h-2h'
            elif 2 <= self.amount < 3:
                return '2h-3h'
            elif 3 <= self.amount < 4:
                return '3h-4h'
            else:
                return '>4h'
        else:
            if self.metric.startswith('weeks'):
                return 'less than a mounth'
            elif self.amount <= 2:
                return 'one to two mounths'
            else:
                print(f'metric={self.metric}')
                return 'three or more mounths'


class Measurement(db.Model):
    __tablename__ = 'measurement'
    measurement_id = db.Column(db.Integer, primary_key=True)
    measurement_type = db.Column(db.String(20), nullable=False)
    measurement_instruments = db.Column(db.String(100), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey(
        'experiment_design.design_id'))
    parent = db.relationship("ExperimentDesign", back_populates="measurements")
