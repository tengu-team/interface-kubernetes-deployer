


# Overview
This interface is used for charms who want to deploy / send resources to a Kubernetes cluster.

# Usage
## Requires
By requiring the `kubernetes-deployer` interface, your charm can create resources on a Kubernetes cluster.

This interface layer will set the following states, as appropriate:
-  `endpoint.{relation-name}.available` flag is set when connected to a providing kubernetes-deployer charm.

Use `send_create_request(request)` to send resource requests. `request` is expected to be a list where each element is a dict which represents a resource.

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

The deployer will respond with a status of the resources by setting the state `endpoint.{relation-name}.new-status`. The Kubernetes worker node ips are available via `get_worker_ips()`.
```python
@when('endpoint.{relation-name}.new-status')
def status_update():
    endpoint = endpoint_from_flag('endpoint.{relation-name}.new-status')
    status = endpoint.get_status()
    ips = endpoint.get_worker_ips()
```

## Provides
By providing  the `kubernetes-deployer` interface, your charm is providing access to a Kubernetes cluster that can be used to create resources.

This interface layer will set the following states, as appropriate:
-  `endpoint.{relation-name}.available` flag is set when at least one relation is active.

You can poll for resource requests via `get_resource_requests()` and send a response back with `send_status(status)`.

```python
@when('endpoint.{relation-name}.available')
def check_resource_requests():
    endpoint = endpoint_from_flag('endpoint.{relation-name}.available')
    resources = endpoint.get_resource_requests()
    # Do stuff with resource
    # Send status updates
    endpoint.send_status(status)
```

## Authors

This software was created in the [IDLab research group](https://www.ugent.be/ea/idlab) of [Ghent University](https://www.ugent.be) in Belgium. This software is used in [Tengu](https://tengu.io), a project that aims to make experimenting with data frameworks and tools as easy as possible.

 - Sander Borny <sander.borny@ugent.be>
