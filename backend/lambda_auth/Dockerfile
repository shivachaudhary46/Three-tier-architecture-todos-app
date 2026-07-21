FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ ${LAMBDA_TASK_ROOT}/shared/
COPY lambda_auth/ ${LAMBDA_TASK_ROOT}/

CMD ["main.handler"]