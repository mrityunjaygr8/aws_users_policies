#!/usr/bin/env python3

import csv
import sys
from pprint import pprint

import boto3


def main(fileName=None):
    # setup boto3 Session
    # extra details such as profile etc can be configured from here
    # see for details: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#guide-configuration
    session = boto3.Session()
    # get a client for just IAM service
    iam = session.client(
        "iam",
    )

    # get iam resource client
    iam_resource = session.resource("iam")

    # generate list of all users into a dict
    user_list = iam.list_users()
    # convert dict into list of users
    user_list = user_list["Users"]
    # empty list to hold values for writing
    user_policy_list = []
    # generate list of all group into a dict
    group_list = iam.list_groups()
    # convert dict into list of users
    group_list = group_list["Groups"]
    # empty list to hold values for writing
    group_policy_list = []

    print("Getting all users and their attached policies. This may take a while")
    # loop over all users
    for x in user_list:
        # get user resource using username
        user = iam_resource.User(x["UserName"])

        # loop over all policies directly attached
        for pol in user.attached_policies.all():
            # create dict to hold username, policy_name and self to signify direct attachment
            user_policy_dict = {
                "username": x["UserName"],
                "policy_name": pol.policy_name,
                "from": "self",
            }
            # append result to user_policy_list
            user_policy_list.append(user_policy_dict)

        # loop over all groups that the user belongs to
        for group in user.groups.all():
            # loop over all policies attached to the group
            for pol in group.attached_policies.all():
            # create dict to hold username, policy_name and name of group
                user_policy_dict = {
                    "username": x["UserName"],
                    "policy_name": pol.policy_name,
                    "from": f"Group {group.name}",
                }
                # append result to user_policy_list
                user_policy_list.append(user_policy_dict)

    print("Getting all groups and their attached policies. This may take a while")
    # loop over all groups
    for x in group_list:
        # get group resource using group name
        group = iam_resource.Group(x["GroupName"])
        # loop over all policies attached to the group
        for pol in group.attached_policies.all():
            # create dict to hold groupname, policy_name
            group_policy_dict = {
                "groupname": x["GroupName"],
                "policy_name": pol.policy_name,
            }
            # append result to group_policy_list
            group_policy_list.append(group_policy_dict)


    print()
    # check if a base-file-name is passed when calling function
    # if base-file-name is passed
    if fileName is not None:
        # create a file called `users_<base-file-name>`
        # and write data of user_policy_list to that file
        with open(f"users_{fileName}", "w+") as f:
            fieldnames = ["username", "policy_name", "from"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(user_policy_list)

        print(f"The user and policies have been saved to users_{fileName} in this directory")
        # create a file called `groups_<base-file-name>`
        # and write data of group_policy_list to that file
        with open(f"groups_{fileName}", "w+") as f:
            fieldnames = ["groupname", "policy_name"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(group_policy_list)

        print(f"The groups and policies have been saved to groups_{fileName} in this directory")

    # if base-file-name is not passed
    # just pretty print the data to console
    else:
        print("Users and Policies")
        pprint(user_policy_list)
        print()
        print("Groups and Policies")
        pprint(user_policy_list)
        print()

        # show usage for saving to file
        print("use `python3 aws_users_policies.py <base_name.csv>` to get")
        print("policies attached to groups in groups_base_name.csv and")
        print("policies attached to users in users_base_name.csv")


if __name__ == "__main__":
    # check if any argument is passed when calling the script
    # if not, pass none so that data will be printed to console
    fileName = sys.argv[1] if len(sys.argv) > 1 else None
    main(fileName)
