from __future__ import print_function
import boto3
import urllib

print('Running function')

glue = boto3.client('glue')

def lambda_handler(event, context):
    gluejobname="job-tech-challenge"

    try:
        runId = glue.start_job_run(JobName=gluejobname)
        status = glue.get_job_run(JobName=gluejobname, RunId=runId['JobRunId'])
        return print("Job Status : ", status['JobRun']['JobRunState'])
    except Exception as e:
        return print(e)
    raise e