#!/usr/bin/env python3
import aws_cdk as cdk

from stacks.app_stack import AppStack


app = cdk.App()

AppStack(app, "AppStack")

cdk.Tags.of(app).add(key="owner", value="ali@datachef.co")
cdk.Tags.of(app).add(key="application", value="FastAPI")

app.synth()
