from enum import Enum
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from coding_tool import db

association_guideline = db.Table('association_guideline', db.metadata,
                                 db.Column('pub_id', db.Integer,
                                           db.ForeignKey('publication.pub_id')),
                                 db.Column('guide_id', db.Integer,
                                           db.ForeignKey('guideline.guide_id')),
                                 )

# association_profile = db.Table('association_profile', db.metadata,
#                                db.Column('profile_id', db.Integer,
#                                          db.ForeignKey('sampling_profile.profile_id')),
#                                db.Column('sample_id', db.Integer,
#                                          db.ForeignKey('sampling.sample_id')),
#                                )

# association_charac = db.Table('association_charac', db.metadata,
#                               db.Column('charac_id', db.Integer,
#                                         db.ForeignKey('sampling_charac.charac_id')),
#                               db.Column('sample_id', db.Integer,
#                                         db.ForeignKey('sampling.sample_id')),
#                               )

# association_task = db.Table('association_task', db.metadata,
#                             db.Column('design_id', db.Integer,
#                                       db.ForeignKey('experiment_design.design_id')),
#                             db.Column('task_id', db.Integer,
#                                       db.ForeignKey('task.task_id')),
#                             )


class Publication(db.Model):
    __tablename__ = 'publication'
    pub_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.String(200), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    keywords = db.Column(db.String(200), nullable=False)
    experiments = db.relationship("Experiment", backref="exp_pub", lazy=True)

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
    lab_settings = db.Column(db.Integer)
    exp_pub_id = db.Column(db.Integer, db.ForeignKey(
        'publication.pub_id'), nullable=False)
    samples = db.relationship("Sampling", backref="exp", lazy=True)
    design = db.relationship("ExperimentDesign", uselist=False,
                             back_populates="experiment")


class ProfileType(Enum):
    PROFESSIONAL = 'Professional'
    GRADSTUDENT = 'Gradstudent'
    UNDERGRADSTUDENT = 'Undergradstudent'
    STUDENT = 'Student'


class RecrutingType(Enum):
    COURSE = 'Course'
    PAID = 'Paid'
    NO_REWARD = 'No reward'
    WORK = 'Work'
    VOLUNTEER = 'Volunteer'
    COMPETITION = 'Competition'


class Recruting(db.Model):
    __tablename__ = 'recruting'
    recruting_id = db.Column(db.Integer, primary_key=True)
    recruiting_strategy = db.Column(db.Enum(RecrutingType), nullable=False)
    parent_recru_id = db.Column(db.Integer, db.ForeignKey(
        'sampling.sample_id'), nullable=False)
    parent = db.relationship(
        "Sampling", back_populates="recruiting_strategies")


class Sampling(db.Model):
    __tablename__ = 'sampling'
    sample_id = db.Column(db.Integer, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey(
        'experiment.exp_id'), nullable=False)
    power_analysis = db.Column(db.Integer, default=0)
    sample_total = db.Column(db.Integer, nullable=False)
    profiles = db.relationship(
        "SamplingProfile", backref="parent_profile", lazy=True)
    characteristics = db.relationship(
        "SamplingCharacteristic", backref="parent_charac", lazy=True)
    recruiting_strategies = db.relationship("Recruting", uselist=False,
                                            backref="parent_recru", lazy=True)
    # characteristics = db.relationship(
    #     'SamplingCharacteristic', secondary=association_charac)

    def __repr__(self):
        return f"Sampling('{self.recruitment_type}', '{self.sample_size}')"

    def sample_classification(self):
        has_student = False
        has_professional = False
        total = 0
        classification = 0
        for a_profile in self.profiles:
            if (a_profile.profile == ProfileType.PROFESSIONAL):
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
    sample_profile_id = db.Column(db.Integer, primary_key=True)
    parent_profile_id = db.Column(
        db.Integer, db.ForeignKey('sampling.sample_id'), nullable=False)
    profile = db.Column(db.Enum(ProfileType), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class SamplingCharacteristic(db.Model):
    __tablename__ = 'sampling_charac'
    charac_id = db.Column(db.Integer, primary_key=True)
    parent_charac_id = db.Column(
        db.Integer, db.ForeignKey('sampling.sample_id'), nullable=False)
    charac = db.Column(db.String(20), nullable=False)
    info = db.Column(db.String(100), nullable=True)


class DesignType(Enum):
    CRD = 'Completely Randomized Desgin'
    PCD = 'Paired Comparison Design'
    TMMAD = 'Two-way Mixed Model ANOVA Design'
    RCBD = 'Randomized Complete Block Design'
    FD = 'Factorial Design'
    IWD = 'Incomplete Within-subjects Design'


class ExperimentDesign(db.Model):
    __tablename__ = 'experiment_design'
    design_id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey(
        'experiment.exp_id'), nullable=False)
    experiment = db.relationship("Experiment", back_populates="design")
    factor_quantity = db.Column(db.Integer, nullable=False)
    design = db.Column(db.Enum(DesignType), nullable=False)
    is_explicity_design = db.Column(db.Integer, nullable=False)
    tasks = db.relationship('Task', backref="task_parent", lazy=True)
    duration = db.relationship("Duration", backref="dura_parent", lazy=True)
    measurements = db.relationship(
        'Measurement', backref='measu_parent', lazy=True)


class TaskType(Enum):
    MAINTENANCE = 'Maintenance'
    CONSTRUCTION = 'Construction'
    TEST = 'Test'
    INSPECTION = 'Inspection'
    COMPREENSION = 'Compreension'
    DESIGN = 'Design'
    DEBUGGING = 'Debuging'


class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True)
    task_parent_id = db.Column(db.Integer, db.ForeignKey(
        'experiment_design.design_id'), nullable=False)
    task_type = db.Column(db.Enum(TaskType), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)


class DurationType(Enum):
    SHORT = 'Short'
    LONG = 'Long'


class Duration(db.Model):
    __tablename__ = 'durantion'
    durantion_id = db.Column(db.Integer, primary_key=True)
    dura_parent_id = db.Column(db.Integer, db.ForeignKey(
        'experiment_design.design_id'), nullable=False)

    # If it is short: this amount is in minutes
    # If it is long: this amount is in months
    durantion_type = db.Column(db.Enum(DurationType))
    amount = db.Column(db.FLOAT)

    def set_amount(self, data, metric):
        self.amount = data
        if metric == 'min' or metric == 'mins':
            self.amount = data / 60
        if metric == 'weeks' or metric == 'week':
            self.amount = data / 4

    def classification(self):
        if self.durantion_type == DurationType.SHORT:
            if self.amount < 1:
                return '>1h'
            elif self.amount < 2:
                return '1h-2h'
            elif self.amount < 3:
                return '2h-3h'
            elif self.amount < 4:
                return '3h-4h'
            else:
                return '>4h'
        else:
            if self.amount < 1:
                return 'less than a mounth'
            elif self.amount <= 2:
                return 'one to two mounths'
            else:
                return 'three or more mounths'


class NatureOfDataSource(Enum):
    TIME = 'Time'
    SOURCE_CODE = 'Source Code'
    SUBJECTIVE = 'Subjective'


class Measurement(db.Model):
    __tablename__ = 'measurement'
    measurement_id = db.Column(db.Integer, primary_key=True)
    measurement_type = db.Column(db.Enum(NatureOfDataSource), nullable=False)
    measurement_instruments = db.Column(db.String(100))
    measu_parent_id = db.Column(db.Integer, db.ForeignKey(
        'experiment_design.design_id'), nullable=False)
