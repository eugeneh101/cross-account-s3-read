import aws_cdk as cdk

from cross_account_s3_read import CrossAccountS3ReadStack


app = cdk.App()
environment = app.node.try_get_context("environment")
env = cdk.Environment(region=environment["AWS_REGION"])
CrossAccountS3ReadStack(
    app,
    "CrossAccountS3ReadStack",
    environment=environment,
    env=env,
)
app.synth()
