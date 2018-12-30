from orm import conn

def patch_conn():

    def mock_execute(sql, args, size=None):
        return sql