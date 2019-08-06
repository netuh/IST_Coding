from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from coding_tool import db

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


class Publication(db.Model):
    __tablename__ = 'publication'
    pub_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.String(200), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    keywords = db.Column(db.String(200), nullable=False)
    samples = db.relationship('Sampling', backref='publication', lazy=True)

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


class Sampling(db.Model):
    __tablename__ = 'sampling'
    sample_id = db.Column(db.Integer, primary_key=True)
    recruiting_strategy = db.Column(db.String(200))
    power_analysis = db.Column(db.Integer, default=0)
    pub_id = db.Column(db.Integer, db.ForeignKey(
        'publication.pub_id'), nullable=False)
    profiles = db.relationship(
        'SamplingProfile', secondary=association_profile)

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
