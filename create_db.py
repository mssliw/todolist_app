from app import app, db

with app.app_context():
    db.create_all()
    print('Database tables:')
    for table in db.metadata.sorted_tables:
        print('- {}'.format(table))

