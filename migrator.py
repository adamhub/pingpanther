import os, sys, sqlite3
from settings import DB_FILE, PINGPANTHER_ROOT


MIGRATION_DIR = os.path.join(PINGPANTHER_ROOT, 'migrations')
sys.path.append(MIGRATION_DIR)


def get_all_migrations():
    """Returns a list of all the migrations inside the MIGRATION_DIR"""
    migrations = os.listdir(MIGRATION_DIR)
    m_list = []
    for m in migrations:
        number = m.split(".")[0]
        file_type = m.split(".")[1]
        if file_type == "py":
            migration_module = __import__(number)
            migration_class = migration_module.Migration
            m_list.append((number, migration_class))
    return sorted(m_list, key=lambda m: m[0])


def run_migrations():
    """Execute each migration's forwards migration"""
    # connect to the database
    db = sqlite3.connect(DB_FILE, detect_types = sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    m_list = get_all_migrations()
    for (number, m_c) in m_list:
        # check if migration has already been migrated
        entry = db.execute("SELECT id FROM migration WHERE id = ? AND migrated = ?", 
                    (number, 1)).fetchone()
        if not entry: # migrate forward
            # print "Migrating %s" % number
            migration = m_c(db)
            migration.forwards()
            db.execute(
                "INSERT INTO migration (id, migrated) VALUES (?, ?)",
                (number, 1))
        # else:
            # print "Skipping %s, already migrated." % number
        db.commit()

