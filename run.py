from coding_tool import create_app
from coding_tool.models import Publication, Guideline, Sampling, SamplingProfile, SamplingCharacteristic, ExperimentDesign, Task, Experiment
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
        e = Experiment(exp_id=exp_id)
        db.session.add(e)
        db.session.commit()
        p = Publication.query.filter_by(pub_id=pub_id).first()
        p.experiments.append(e)
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
        p = Experiment.query.get(int(sample_id))
        # p = Experiment.query.filter_by(exp_id=sample_id).first()
        print(f'experiment = {p}')
        s = Sampling(sample_id=sample_id, recruiting_strategy=recruiting_strategy,
                     power_analysis=power_analysis)
        s.exp_id = int(sample_id)
        for profile in sample_profile.split(';'):
            p = profile.split(':')
            a = SamplingProfile(profile=p[0], quantity=int(p[1]))
            s.profiles.append(a)

        if isinstance(sample_characteristics, str):
            for charac in sample_characteristics.lower().split(';'):
                print(f'charac={charac.replace(" ", "")}')
                p = charac.replace(" ", "").split(':')
                if len(p) > 1:
                    a = SamplingCharacteristic(charac=p[0], info=p[1])
                else:
                    a = SamplingCharacteristic(charac=p[0])
                s.characteristics.append(a)
        db.session.add(s)
        db.session.commit()


def seed_design():
    file_name = os.path.join(
        static_file_dir, 'coding_tool', 'static', 'csv', 'doe.csv')
    # Read CSV with Pandas
    with open(file_name, 'r') as file:
        df = pd.read_csv(file, sep='|')
    for index, row in df.iterrows():
        paper_id = int(row['paper_id'])
        factor_quantity = int(row['factor_quantity'])
        design = row['design']
        explicity_design = row['explicity_design']
        tasks = row['tasks']
        trial_duration = row['trial_duration']
        s = ExperimentDesign(factor_quantity=factor_quantity, design=design,
                             is_explicity_design=explicity_design)
        # paper_id|factor_quantity|design|explicity_design|tasks|trial_duration


@app.before_first_request
def before_first_request_func():
    seed_publication()
    seed_guidelines()
    seed_experiments()
    seed_sampling()
    # seed_design()


if __name__ == '__main__':
    app.run(debug=True)
