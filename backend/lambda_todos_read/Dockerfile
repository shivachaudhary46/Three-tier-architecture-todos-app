FROM public.ecr.aws/lambda/python:3.12 
WORKDIR ${lAMBDA_TASK_ROOT}
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared/ ${lAMBDA_TASK_ROOT}/shared/
COPY lambda_todos_read/ ${lAMBDA_TASK_ROOT}/
CMD ["main.handler"]
