#!/usr/bin/env python3

import boto3


def main():
    iam = boto3.client("iam")
    user_list = iam.list_users()
    print(user_list["Users"])


if __name__ == "__main__":
    main()
