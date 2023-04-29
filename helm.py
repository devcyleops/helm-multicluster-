import os
from kubernetes import client, config
from helm import Helm

# Set up the Kubernetes API client
config.load_kube_config()

# Define the list of clusters to manage
clusters = [
    {
        'name': 'cluster1',
        'url': 'https://cluster1.example.com',
        'ca_cert': '/path/to/cluster1/ca.crt',
        'token': 'cluster1-token',
        'namespace': 'default'
    },
    {
        'name': 'cluster2',
        'url': 'https://cluster2.example.com',
        'ca_cert': '/path/to/cluster2/ca.crt',
        'token': 'cluster2-token',
        'namespace': 'default'
    },
    {
        'name': 'cluster3',
        'url': 'https://cluster3.example.com',
        'ca_cert': '/path/to/cluster3/ca.crt',
        'token': 'cluster3-token',
        'namespace': 'default'
    }
]

# Loop through the list of clusters and perform actions on each one
for cluster in clusters:
    print(f"Managing cluster '{cluster['name']}'")

    # Set up the Kubernetes API client for this cluster
    configuration = client.Configuration()
    configuration.host = cluster['url']
    configuration.ssl_ca_cert = cluster['ca_cert']
    configuration.verify_ssl = True
    configuration.api_key = {
        'authorization': f'Bearer {cluster["token"]}'
    }
    client.Configuration.set_default(configuration)

    # Create a Helm client for this cluster
    helm = Helm(namespace=cluster['namespace'])

    # Example actions:
    # - List all namespaces in this cluster
    namespaces = client.CoreV1Api().list_namespace().items
    print(f"Namespaces in cluster '{cluster['name']}':")
    for namespace in namespaces:
        print(f"- {namespace.metadata.name}")

    # - Install a chart in this cluster
    helm.install(
        chart='nginx',
        release_name='nginx',
        values={
            'image': 'nginx:latest',
            'replicas': 3
        }
    )

    # - Upgrade a chart in this cluster
    helm.upgrade(
        chart='nginx',
        release_name='nginx',
        values={
            'image': 'nginx:latest',
            'replicas': 5
        }
    )

    # - Uninstall a chart in this cluster
    helm.uninstall(release_name='nginx')
