from data.db_session import global_init, create_session
from data.users import User

db_name = input()
global_init(db_name)
db_sess = create_session()
users = db_sess.query(User).filter(User.position.like("%chief%") | User.position.like("%middle%"))
for user in users:
    print(user, user.position)
