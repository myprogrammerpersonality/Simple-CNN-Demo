import os
from constructs import Construct
from aws_cdk import (
    Stack,
    Duration,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
)


class AppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Add Lambda function
        fastapi_cdk_function = lambda_.Function(
            self,
            "FastAPIFunction",
            code=lambda_.Code.from_asset_image("./assets"),
            handler=lambda_.Handler.FROM_IMAGE,
            runtime=lambda_.Runtime.FROM_IMAGE,
            environment={
                "VAR": "TEST",
            },
            timeout=Duration.seconds(30),
            # Set this to 8GB
            memory_size=8192,
        )

        # Add API Gateway
        api = apigateway.RestApi(
            self,
            "FastAPIAPI",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
            ),
        )

        # Add a resource to the API Gateway
        fastapi_cdk_function_integration = apigateway.LambdaIntegration(
            fastapi_cdk_function, allow_test_invoke=False
        )

        # Add a method to the resource
        api.root.add_method("ANY", fastapi_cdk_function_integration)

        api.root.add_proxy(
            default_integration=apigateway.LambdaIntegration(
                fastapi_cdk_function, allow_test_invoke=False
            ),
            any_method=True,
        )
