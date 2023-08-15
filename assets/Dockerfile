FROM public.ecr.aws/lambda/python:3.11

# Copy function code
COPY ./ ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the environment variable for the model weights download directory
ENV TORCH_HOME=/var/task/torch_cache

# Download the model weights directly to a writable directory
RUN python3 -c "from torchvision.models.detection import fasterrcnn_resnet50_fpn; fasterrcnn_resnet50_fpn(pretrained=True)"

# Set proper permissions for the torch_cache directory
RUN chmod -R 755 $TORCH_HOME

# Set WORKDIR to app
WORKDIR /var/task/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.lambda_handler" ]
