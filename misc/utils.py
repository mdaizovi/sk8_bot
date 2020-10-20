from django.db import connection, reset_queries

def num_queries(reset=True, string_marker=None):
    """
    Prints number of db queries. Used for minimizing db hits, put this wherever you want a tally.
    """
    if string_marker:
        print(string_marker, ": ", str(len(connection.queries)))
    else:
        print(len(connection.queries))
    if reset:
        reset_queries()