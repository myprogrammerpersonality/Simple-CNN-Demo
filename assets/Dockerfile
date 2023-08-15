FROM public.ecr.aws/lambda/python:3.10

# Copy function code
COPY ./ ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Download the model weights directly to a writable directory
ENV TORCH_HOME=/var/task/torch_cache
RUN python3 -c "from torchvision.models.detection import fasterrcnn_mobilenet_v3_large_320_fpn; fasterrcnn_mobilenet_v3_large_320_fpn(pretrained=True)"

# Set WORKDIR to app
WORKDIR /var/task/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.lambda_handler" ]
