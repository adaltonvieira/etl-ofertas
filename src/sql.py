import sys
from db import get_connection

conn = get_connection()
for row in conn.execute(sys.argv[1]):
    print(dict(row))
conn.close()
