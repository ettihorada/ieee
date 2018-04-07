
import argparse
import json, codecs
from ieee_client import IeeeClient

# import MySQLdb

# class LocalSQL:
#     host = ""
#     user = ""
#     password = ""
#     db = ""
#
#
# def port_to_sql(list_of_articles):
#
#     for ar in list_of_articles["articles"]:
#         print("i am inserting {}".format(ar))
#
#     conn = MySQLdb.connect(host=LocalSQL.host,
#                            user=LocalSQL.user,
#                            passwd=LocalSQL.password,
#                            db=LocalSQL.db)
#     cursor = conn.cursor()
#     for article in list_of_articles:
#         cursor.execute("INSERT INTO ieee (abstract, title, pdf_url, authors, index_terms, publication_title, conference_dates) VALUES ({abstract},{title},{pdf_url},{authors},{index_terms},{publication_title}, {conference_dates})".format(**article))

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
                        required=True,
                        help='File path to output of desired RE articles from ieee')

    args = parser.parse_args()

    client = IeeeClient(args.apikey)
    if args.bootstrap:
        client.maximum_results(args.max_records)
        client.query_text('re')
    else:
        raise NotImplementedError("Collecting by date wasn't implemented")
        client.search_latest(args.from_date, args.to_date)

    data = client.run()

    with open(args.output, 'wb') as f:
        json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False)
    # port_to_sql(client.run())


if __name__ == "__main__":
    main()
