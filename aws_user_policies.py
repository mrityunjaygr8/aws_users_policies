#!/usr/bin/env python3

import csv
import sys
from pprint import pprint

import boto3


def main(fileName=None):
    print("Getting all users and their attached policies. This may take a while")
    session = boto3.Session(profile_name="der")
    iam = session.client(
        "iam",
    )
    iam_user = session.resource("iam")
    user_list = iam.list_users()
    user_list = user_list["Users"]
    user_policy_list = []

    for x in user_list:
        user = iam_user.User(x["UserName"])
        for pol in user.attached_policies.all():
            user_policy_dict = {
                "username": x["UserName"],
                "policy_name": pol.policy_name,
                "from": "self",
            }
            user_policy_list.append(user_policy_dict)

        for group in user.groups.all():
            for pol in group.attached_policies.all():
                user_policy_dict = {
                    "username": x["UserName"],
                    "policy_name": pol.policy_name,
                    "from": f"Group {group.name}",
                }
                user_policy_list.append(user_policy_dict)

    if fileName is not None:
        with open(fileName, "w+") as f:
            fieldnames = ["username", "policy_name", "from"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(user_policy_list)

        print(f"The user and policies have been saved to {fileName} in this directory")

    else:
        pprint(user_policy_list)


if __name__ == "__main__":
    fileName = sys.argv[1] if len(sys.argv) > 1 else None
    main(fileName)
