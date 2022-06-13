from armada_client.client import ArmadaClient
import grpc

from armada_client.k8s.io.api.core.v1 import generated_pb2 as core_v1
from armada_client.k8s.io.apimachinery.pkg.api.resource import (
    generated_pb2 as api_resource,
)

from armada_client.armada import (
    submit_pb2,
)


def submit_sleep_job():
    pod = core_v1.PodSpec(containers=[
        core_v1.Container(
            name="sleep",
            image="busybox",
            args=["sleep", "100s"],
            securityContext=core_v1.SecurityContext(runAsUser=1000),
            resources=core_v1.ResourceRequirements(
                requests={
                    "cpu": api_resource.Quantity(string="120m"),
                    "memory": api_resource.Quantity(string="510Mi"),
                },
                limits={
                    "cpu": api_resource.Quantity(string="120m"),
                    "memory": api_resource.Quantity(string="510Mi"),
                },
            ),
        )
    ],
    )

    return [submit_pb2.JobSubmitRequestItem(priority=1, pod_spec=pod)]

if __name__ == "__main__":
    tester = ArmadaClient(
        grpc.insecure_channel(target="127.0.0.1:50051")
    )
#    tester.create_queue(name='test',priority_factor=1)
    job = tester.submit_jobs(queue='test', job_set_id='job-set-1',
                       job_request_items=submit_sleep_job())

    job_id = job.job_response_items[0].job_id

    return_val = tester.watch_events(queue='test', job_set_id='job_set-1')
    for event in return_val:
        print(event)
