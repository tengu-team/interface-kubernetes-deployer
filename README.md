
# Overview
This interface is used for charms who want to deploy / send resources to a Kubernetes cluster.

# Usage
## Requires
By requiring the `kubernetes-deployer` interface, your charm can create resources on a Kubernetes cluster.  As soon as the `endpoint.{relation-name}.available` state is, your charm can send resource requests via `send_create_request(request)`.

`send_create_request(request)` expects `request` to be a list where each element is a dict which represents a resource.

As an example, if we would want to deploy resources defined in `charm_dir() + '/files/resources.yaml'`:
```python
@when('endpoint.{relation-name}.available')
def deploy_app():
    endpoint = endpoint_from_flag('endpoint.{relation-name}.available')
    resources = []
    with open(charm_dir() + '/files/resources.yaml', 'r') as f:
        docs = yaml.load_all(f)
        for doc in docs:
            resources.append(doc)
    endpoint.send_create_request(resources)
```

The deployer will respond with a status of the resources by setting the state `endpoint.{relation-name}.new-status`.
```python
@when('endpoint.{relation-name}.new-status')
def status_update():
    endpoint = endpoint_from_flag('endpoint.{relation-name}.new-status')
    status = endpoint.get_status()
```

## Provides
By providing  the `kubernetes-deployer` interface, your charm is providing access to a Kubernetes cluster that can be used to create resources.

When the  `endpoint.{relation-name}.available` state is set, you can poll for resource requests via `get_resource_requests()` and send a response back with `send_status(status)`.

A trivial example is:
```python
@when('endpoint-{relation-name}.available')
def check_resource_requests():
    endpoint = endpoint_from_flag('endpoint-{relation-name}.available')
    resources = endpoint.get_resource_requests()
    # Do stuff with resource
    # Send status updates
    endpoint.send_status(status)
```

## Authors

This software was created in the [IDLab research group](https://www.ugent.be/ea/idlab) of [Ghent University](https://www.ugent.be) in Belgium. This software is used in [Tengu](https://tengu.io), a project that aims to make experimenting with data frameworks and tools as easy as possible.

 - Sander Borny <sander.borny@ugent.be>
