#!/usr/bin/python3

import urllib.request, urllib.error
import colorama
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Generate HTTP requests to provided host")
    parser.add_argument("-a", "--address", help="Address of tested host", required=True)
    parser.add_argument("-n", "--number", help="Number of requests", default=100, type=int)

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()

    successful_conn, dropped_conn, no_content_conn = 0, 0, 0
    count = args["number"]
    address = args["address"]

    for _ in range(count):
        try:
            contents = urllib.request.urlopen(address).read()
            if contents is not None:
                successful_conn += 1
            else:
                no_content_conn += 1
        except urllib.error.URLError:
            dropped_conn += 1
            pass

    print(f"{'Connections' : ^20}{'Number' : ^7}")

    print(f"{'Successful:' : <20}{colorama.Fore.GREEN}{successful_conn : ^7}{colorama.Style.RESET_ALL}")
    print(f"{'No-content-received:' : <20}{colorama.Fore.YELLOW}{no_content_conn : ^7}{colorama.Style.RESET_ALL}")
    print(f"{'Dropped:' : <20}{colorama.Fore.RED}{dropped_conn : ^7}{colorama.Style.RESET_ALL}")