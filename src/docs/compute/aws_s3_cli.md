# AWS S3 CLI

## Setup

Install:
```shell
$ pip install awscli awscli-plugin-endpoint awscrt
```
Configure (here with OVHcloud as backend):
```shell
$ cat ~/.aws/config
[plugins]
endpoint = awscli_plugin_endpoint

[profile my-profile-name]
region = gra
s3 =
  endpoint_url = https://s3.gra.io.cloud.ovh.net/
  signature_version = s3v4
s3api =
  endpoint_url = https://s3.gra.io.cloud.ovh.net/



$ cat ~/.aws/credentials
[my-profile-name]
aws_access_key_id = <access key>
aws_secret_access_key = <secret key>
```

## List objects

```shell
$ aws s3 ls s3://my-bucket-name --human-readable --summarize --recursive --profile my-profile-name
```
```
2024-11-30 03:30:25    1.1 MiB foobar/2024-11-28.zst
2024-12-01 03:01:17    1.1 MiB foobar/2024-11-29.zst
...

Total Objects: 96
   Total Size: 64.9 MiB
```

## List objects versions

In case bucket is versioned:
```shell
$ aws s3api list-object-versions --bucket my-bucket-name --profile my-profile-name
{
    "Versions": [
        {
            "ETag": "\"866f2973a36c3505c37d3959e24eba37\"",
            "Size": 409011,
            "StorageClass": "STANDARD",
            "Key": "foobar/2024-11-28.zst",
            "VersionId": "1732933825.600330",
            "IsLatest": false,
            "LastModified": "2024-11-30T02:30:25.000Z",
            "Owner": {
                "DisplayName": "12345:user-xxx",
                "ID": "12345:user-xxx"
            }
        },
        {
            "ETag": "\"5e85b9d1b17904f3d0c6253eeab722f6\"",
            "Size": 1180297,
            "StorageClass": "STANDARD",
            "Key": "foobar/2024-11-28.zst",
            "VersionId": "1732934824.643878",
            "IsLatest": true,
            "LastModified": "2024-11-31T02:30:25.000Z",
            "Owner": {
                "DisplayName": "12345:user-xxx",
                "ID": "12345:user-xxx"
            }
        },
        ...
    ]
}
```

## Get objects

```shell
$ aws s3api head-object --bucket my-bucket-name --key foobar/2025-01-14.zst --profile my-profile-name
```
```json
{
    "AcceptRanges": "bytes",
    "LastModified": "Thu, 16 Jan 2025 03:58:27 GMT",
    "ContentLength": 400257,
    "ETag": "\"0787c4c4238c8924a8ca7f6b83094a4c\"",
    "VersionId": "1736999907.007856",
    "ContentType": "binary/octet-stream",
    "Metadata": {},
    "ReplicationStatus": "COMPLETED"
}
```

## Upload objects

```shell
$ aws s3 cp /home/me/some_file s3://my-bucket-name/some_path/somefile --profile my-profile-name
```

## Download objects

```shell
$ aws s3 cp s3://my-bucket-name/some_path/somefile /home/me/some_file --profile my-profile-name
```

## Delete objects

```shell
# --version-id is needed if bucket is versioned, otherwise you will just create a new "empty" version of the object without deleting the "real" file
$ aws s3api delete-object --bucket my-bucket-name --key foobar/2025-01-14.zst --version-id 1729673115.690901 --profile my-profile-name
```

## Replication setup

Create a local file (eg `bucket-replica-config.json`) with bucket replication config:
```json
{
  "Role": "arn:aws:iam::1234566:role/s3-replication",
  "Rules": [
    {
      "ID": "my_replication_name",
      "Priority": 1,
      "Filter": {},
      "Status": "Enabled",
      "Destination": {
        "Bucket": "arn:aws:s3:::my-destination-bucket"
      },
      "DeleteMarkerReplication": {
        "Status": "Enabled"
      }
    }
  ]
}
```
Apply it:
```shell
$ aws s3api put-bucket-replication --replication-configuration "file://bucket-replica-config.json" --bucket my-bucket-name --profile my-profile-name
```
Ensure it's OK:
```shell
$ aws s3api get-bucket-replication --bucket my-bucket-name --profile my-profile-name
```
```json
{
    "ReplicationConfiguration": {
        "Role": "arn:aws:iam::1234566:role/s3-replication",
        "Rules": [
            {
                "ID": "my_replication_name",
                "Priority": 1,
                "Filter": {},
                "Status": "Enabled",
                "Destination": {
                    "Bucket": "arn:aws:s3:::my-destination-bucket"
                },
                "DeleteMarkerReplication": {
                    "Status": "Enabled"
                }
            }
        ]
    }
}
```

## Generate download URL

```shell
aws s3 presign s3://my-bucket-name/foobar/2024-01-02.zst --expires-in 604800 --profile my-profile-name
```
```
https://s3.gra.io.cloud.ovh.net/my-bucket-name/foobar/2024-01-02.zst?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...
```

## Debug

```shell
$ aws --debug s3api get-object ...
```
