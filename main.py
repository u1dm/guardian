from crud import DatabaseManager

db = DatabaseManager()
db.create_user('asd', 'super_passwd')
db.add_user_password('asd', 'super_passwd', 'linkfrg', 'alololo')
print(db.get_user_password('asd', 'super_passwd', 'linkfrg'))