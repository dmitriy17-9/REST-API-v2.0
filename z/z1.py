db_name = input()
global_init(db_name)
db_sess = create_session()
users = db_sess.query(User).filter(User.address == "module_1")
for user in users:
    print(user)