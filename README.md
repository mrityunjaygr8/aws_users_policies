### Script to show the policies attached to users and groups

#### Setup

install dependencies using

```bash
pip install -r requirements.txt
```

#### Usage

To print the attached policies on the console.

```python3
python3 aws_users_policies.py
```

To save the attached policies in dedicated files:

```python3

python3 aws_users_policies.py <base-file-name.csv>
```

This will create 2 files in the current working directory
`users_base-file-name.csv` for policies attached/inherited by users
`groups_base-file-name.csv` for policies attached to groups

#### Authentication

Authentication will be handled by [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration)
