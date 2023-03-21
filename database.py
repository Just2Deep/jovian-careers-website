from sqlalchemy import create_engine, text
import os

my_db_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(my_db_string)


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))

    jobs = []
    for row in result.all():

      jobs.append(row._asdict())

  return jobs


def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs where id = :val"),
                          {"val": id})

    row = result.all()
    if row:
      return row[0]._asdict()
    else:
      return None


def add_application_to_db(job_id, application):
  with engine.connect() as conn:
    query = text(
      "INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url);"
    )
    parameters = {
      "job_id": job_id,
      "full_name": application['full_name'],
      "email": application['email'],
      "linkedin_url": application['linkedin_url'],
      "education": application['education'],
      "work_experience": application['work_experience'],
      "resume_url": application['resume_url'],
    }
    print(query)
    conn.execute(query, parameters)
    conn.commit()
