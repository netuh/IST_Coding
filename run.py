from coding_tool import create_app
from coding_tool.models import *
from coding_tool import db
import pandas as pd
import os

app = create_app()

static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)))


def seed_publication():
    file_name = os.path.join(
        static_file_dir, 'coding_tool', 'static', 'csv', 'publications.csv')
    # Read CSV with Pandas
    with open(file_name, 'r') as file:
        df = pd.read_csv(file, sep='|')

    engine = db.get_engine()
    df.to_sql('publication',
              con=engine,
              index=False,
              index_label='id',
              if_exists='replace')


def seed_experiments():
    file_name = os.path.join(
        static_file_dir, 'coding_tool', 'static', 'csv', 'experiment_map.csv')
    # Read CSV with Pandas
    with open(file_name, 'r') as file:
        df = pd.read_csv(file, sep='|')
    for index, row in df.iterrows():
        exp_id = int(row['exp_id'])
        pub_id = int(row['pub_id'])
        lab_settings = int(row['lab_settings'])
        p = Publication.query.get(exp_id)
        e = Experiment(exp_id=exp_id, lab_settings=lab_settings, pub=p)
        db.session.add(e)
    db.session.commit()


def seed_guidelines():
    file_name = os.path.join(
        static_file_dir, 'coding_tool', 'static', 'csv', 'guidelines.csv')
    # Read CSV with Pandas
    with open(file_name, 'r') as file:
        df = pd.read_csv(file, sep='|')

    for index, row in df.iterrows():
        guide_id = int(row['guide_id'])
        paper_id = int(row['paper_id'])
        title = row['title']
        year = row['year']
        authors = row['authors']
        address = row['address']
        g = Guideline.query.get(guide_id)
        if not g:
            g = Guideline(guide_id=guide_id, title=title, year=year,
                          authors=authors, address=address)
            db.session.add(g)
            db.session.commit()
        p = Publication.query.filter_by(pub_id=paper_id).first()
        g.referenced_by.append(p)
    db.session.commit()


def seed_sampling():
    list_e = Experiment.query.all()
    file_name = os.path.join(
        static_file_dir, 'coding_tool', 'static', 'csv', 'sampling.csv')
    # Read CSV with Pandas
    with open(file_name, 'r') as file:
        df = pd.read_csv(file, sep='|')
    for index, row in df.iterrows():
        sample_id = int(row['sample_id'])
        pub_id = int(row['pub_id'])
        sample_profile = row['sample_profile']
        sample_characteristics = row['sample_characteristics']
        recruiting_strategy = row['recruiting_strategy']
        power_analysis = row['power_analysis']
        total = 0
        p = Experiment.query.get(int(sample_id))
        s = Sampling(sample_id=sample_id, sample_total=total,
                     power_analysis=power_analysis)
        s.exp_id = int(sample_id)
        if isinstance(recruiting_strategy, str):
            for strategy in recruiting_strategy.split(';'):
                r = Recruting(recruiting_strategy=RecrutingType(
                    strategy.capitalize()))
                r.parent = s
        for profile in sample_profile.split(';'):
            p = profile.replace(" ", "").split(':')
            a = SamplingProfile(profile=ProfileType(
                p[0].capitalize()), quantity=int(p[1]))
            total += int(p[1])
            s.profiles.append(a)
        if isinstance(sample_characteristics, str):
            for charac in sample_characteristics.lower().split(';'):
                p = charac.replace(" ", "").split(':')
                if len(p) > 1:
                    a = SamplingCharacteristic(charac=p[0], info=p[1])
                else:
                    a = SamplingCharacteristic(charac=p[0])
                s.characteristics.append(a)
        s.sample_total = total
        db.session.add(s)
        db.session.commit()


def seed_design():
    file_name = os.path.join(
        static_file_dir, 'coding_tool', 'static', 'csv', 'doe.csv')
    # Read CSV with Pandas
    with open(file_name, 'r') as file:
        df = pd.read_csv(file, sep='|')
    for index, row in df.iterrows():
        exp_id = int(row['exp_id'])
        factor_quantity = int(row['factor_quantity'])
        design = row['design']
        explicity_design = row['explicity_design']
        tasks = row['tasks']
        trial_duration = row['trial_duration']
        s = ExperimentDesign(factor_quantity=factor_quantity, design=DesignType(design),
                             is_explicity_design=explicity_design)
        p = Experiment.query.get(int(exp_id))
        p.design = s

        for profile in tasks.split(';'):
            p = profile.replace(" ", "").split(':')
            a = Task(task_type=TaskType(p[0].capitalize()), quantity=int(p[1]))
            s.tasks.append(a)
            db.session.add(a)
        if isinstance(trial_duration, str):
            data = trial_duration.split(':')
            amount = data[1].split('-')
            d = Duration(durantion_type=DurationType(data[0]))
            d.set_amount(metric=amount[1], data=float(amount[0]))
            s.duration = d
            db.session.add(d)
        db.session.add(s)
        db.session.commit()


def seed_measuriments():
    file_name = os.path.join(
        static_file_dir, 'coding_tool', 'static', 'csv', 'measurements.csv')
    # Read CSV with Pandas
    with open(file_name, 'r') as file:
        df = pd.read_csv(file, sep='|')
    for index, row in df.iterrows():
        exp_id = int(row['exp_id'])
        m_type = row['type']
        m_instrument = row['instrument']
        m = Measurement(measurement_instruments=m_instrument,
                        measurement_type=NatureOfDataSource(m_type))
        p = Experiment.query.get(exp_id)
        db.session.add(m)
        p.measurements = m
    db.session.commit()


@app.before_first_request
def before_first_request_func():
    seed_publication()
    seed_guidelines()
    seed_experiments()
    seed_sampling()
    seed_design()
    seed_measuriments()


if __name__ == '__main__':
    app.run(debug=True)
