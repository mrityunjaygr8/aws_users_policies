#!/usr/bin/env python3

import csv
import sys
from pprint import pprint

import boto3


def main(fileName=None):
    session = boto3.Session()
    iam = session.client(
        "iam",
    )
    iam_resource = session.resource("iam")
    user_list = iam.list_users()
    user_list = user_list["Users"]
    user_policy_list = []
    group_list = iam.list_groups()
    group_list = group_list["Groups"]
    group_policy_list = []

    print("Getting all users and their attached policies. This may take a while")
    for x in user_list:
        user = iam_resource.User(x["UserName"])
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

    print("Getting all groups and their attached policies. This may take a while")
    for x in group_list:
        group = iam_resource.Group(x["GroupName"])
        for pol in group.attached_policies.all():
            group_policy_dict = {
                "groupname": x["GroupName"],
                "policy_name": pol.policy_name,
            }
            group_policy_list.append(group_policy_dict)


    print()
    if fileName is not None:
        with open(f"users_{fileName}", "w+") as f:
            fieldnames = ["username", "policy_name", "from"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(user_policy_list)

        print(f"The user and policies have been saved to users_{fileName} in this directory")
        with open(f"groups_{fileName}", "w+") as f:
            fieldnames = ["groupname", "policy_name"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(group_policy_list)

        print(f"The groups and policies have been saved to groups_{fileName} in this directory")

    else:
        print("Users and Policies")
        pprint(user_policy_list)
        print()
        print("Groups and Policies")
        pprint(user_policy_list)
        print()

        print("use `python3 aws_users_policies.py <base_name.csv>` to get")
        print("policies attached to groups in groups_base_name.csv and")
        print("policies attached to users in users_base_name.csv")


if __name__ == "__main__":
    fileName = sys.argv[1] if len(sys.argv) > 1 else None
    main(fileName)
