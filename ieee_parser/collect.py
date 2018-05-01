
import argparse
import json, codecs
from ieee_parser.ieee_client import IeeeClient
from sqlalchemy import create_engine

SQL_PARAMS = {
    "host_name": "localhost",
    "user_name": "root",
    "password": "",
    "database": "ieeeconfs"
}
# DB NAME ieeeconfs
def port_to_sql(list_of_articles):
    engine = create_engine("mysql://{user_name}@{host_name}/{database}".format(**SQL_PARAMS))
    conn = engine.connect()

    terms = set([term for article in list_of_articles for term in article["index_terms"]])
    for term in terms:
        conn.execute("INSERT INTO Keywords (text) VALUES (\'{}\')".format(term))

    full_name = set([auter for article in list_of_articles for auter in article["authors"]])
    for auter in full_name:
        conn.execute("INSERT INTO authors (FullName) VALUES (\'[{}]\')".format(auter))



    # conn.execute("INSERT INTO Keywords (abstract, title, pdf_url, authors, index_terms, publication_title, conference_dates) VALUES ({abstract},{title},{pdf_url},{authors},{index_terms},{publication_title}, {conference_dates})".format(**article))


def main():
    parser = argparse.ArgumentParser(description='Run ieee collector')
    parser.add_argument('-a', '--apikey',
                        required=True,
                        help='Official api key')
    parser.add_argument('-b', '--bootstrap',
                        required=False,
                        action='store_true',
                        default=False,
                        help='Collect all possible articles along the history')
    parser.add_argument('-f', '--from-date',
                        required=False,
                        default=None,
                        help='Set from date e.g. 20180314')
    parser.add_argument('-t', '--to-date',
                        required=False,
                        default=None,
                        help='Set to date e.g. 20180314')
    parser.add_argument('-m', '--max-records',
                        required=False,
                        default=500,
                        help='Up to 1000 records are allowed')
    parser.add_argument('-o', '--output',
                        required=False,
                        default=None,
                        help='File path to output of desired RE articles from ieee')
    parser.add_argument('-d', '--db',
                        action='store_true',
                        default=False,
                        help='File path to output of desired RE articles from ieee')

    args = parser.parse_args(["-a", "gg6gz9zkeqw6nbrkj7dg692t", "-b", "-db"])

    client = IeeeClient(args.apikey)
    if args.bootstrap:
        client.maximum_results(args.max_records)
        client.query_text('re')
    else:
        raise NotImplementedError("Collecting by date wasn't implemented")
        client.search_latest(args.from_date, args.to_date)

    data = client.run()

    if args.db:
        port_to_sql(data)
    elif args.output is not None:
        with open(args.output, 'wb') as f:
            json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False)
    else:
        import pprint
        pprint.pprint(data)


if __name__ == "__main__":
    main()
