# Sprelf ImageHost

A simple image hosting service.

Create the backend stack using the provided CloudFormation template.

Install locally:

```
pip install -e <this directory>
```

To configure settings, create a `settings.yaml` file in the directory `~/.sprelf/imghost/`:

```yaml
aws_profile: <AWS CLI profile to use>
table_name: <Name of the DynamoDB table>
domain: <Domain name>
```

Upload images and generate links with the following command:

```
sprelf-img <image path> (--custom <custom link>)
```
