db_name = input()
global_init(db_name)
db_sess = create_session()
jobs = db_sess.query(Jobs).filter(Jobs.work_size < 20, Jobs.is_finished == 0)
for job in jobs:
    print(job)
