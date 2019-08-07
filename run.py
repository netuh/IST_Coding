from coding_tool import create_app
from coding_tool.models import Publication, Guideline, Sampling, SamplingProfile, SamplingCharacteristic
from coding_tool import db
import pandas as pd
import os


app = create_app()
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)))


@app.before_first_request
def before_first_request_func():
  seed_publication()
  seed_guidelines()
  seed_sampling()


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
    p = Publication.query.filter_by(pub_id=pub_id).first()
    s = Sampling(sample_id=sample_id, recruiting_strategy=recruiting_strategy,
                 power_analysis=power_analysis)
    p.samples.append(s)
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


if __name__ == '__main__':
  app.run(debug=True)
