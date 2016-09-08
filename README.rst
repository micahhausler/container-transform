.. image:: https://travis-ci.org/micahhausler/container-transform.png
   :target: https://travis-ci.org/micahhausler/container-transform

.. image:: https://coveralls.io/repos/micahhausler/container-transform/badge.png?branch=master
    :target: https://coveralls.io/r/micahhausler/container-transform?branch=master

.. image:: https://readthedocs.org/projects/container-transform/badge/?version=latest
    :target: http://container-transform.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status


container-transform
===================
container-transform is a small utility to transform various docker container
formats to one another.

Currently, container-transform can parse and convert:

* Kubernetes Pod specs
* ECS task definitions
* Docker-compose configuration files
* Marathon Application Definitions or Groups of Applications
* Chronos Task Definitions

and it can output to:

* Systemd unit files


Examples
--------

Compose to Kubernetes
~~~~~~~~~~~~~~~~~~~~~

::

    $ cat docker-compose.yaml
    version: '2'
    services:
      etcd:
        cpu_shares: 102.4
        entrypoint: /usr/local/bin/etcd -data-dir /var/etcd/data -listen-client-urls http://127.0.0.1:2379,http://127.0.0.1:4001
          -advertise-client-urls http://127.0.0.1:2379,http://127.0.0.1:4001 -initial-cluster-token
          skydns-etcd
        image: gcr.io/google_containers/etcd-amd64:2.2.1
        mem_limit: 524288000b
      healthz:
        command: -cmd=nslookup kubernetes.default.svc.cluster.local 127.0.0.1 >/dev/null
          -port=8080
        cpu_shares: 10.24
        image: gcr.io/google_containers/exechealthz:1.0
        mem_limit: 20971520b
        ports:
        - '8080'
      kube2sky:
        command: --kubecfg-file=/etc/kubernetes/worker-kubeconfig.yaml --domain=cluster.local
        cpu_shares: 102.4
        image: gcr.io/google_containers/kube2sky:1.14
        mem_limit: 209715200b
        volumes:
        - /usr/share/ca-certificates:/etc/ssl/certs
        - /etc/kubernetes/worker-kubeconfig.yaml:/etc/kubernetes/worker-kubeconfig.yaml:ro
        - /etc/kubernetes/ssl:/etc/kubernetes/ssl:ro
      skydns:
        command: -machines=http://127.0.0.1:4001 -addr=0.0.0.0:53 -ns-rotate=false -domain=cluster.local.
        cpu_shares: 102.4
        image: gcr.io/google_containers/skydns:2015-10-13-8c72f8c
        mem_limit: 209715200b
        ports:
        - 53/udp
        - '53'
    $ container-transform -i compose -o kubernetes docker-compose.yaml
    apiVersion: extensions/v1beta1
    kind: Deployment
    metadata:
      labels:
        app: null
        version: latest
      name: null
      namespace: default
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: null
          version: latest
      template:
        metadata:
          labels:
            app: null
            version: latest
        spec:
          containers:
          - command:
            - /usr/local/bin/etcd
            - -data-dir
            - /var/etcd/data
            - -listen-client-urls
            - http://127.0.0.1:2379,http://127.0.0.1:4001
            - -advertise-client-urls
            - http://127.0.0.1:2379,http://127.0.0.1:4001
            - -initial-cluster-token
            - skydns-etcd
            image: gcr.io/google_containers/etcd-amd64:2.2.1
            name: etcd
            resources:
              limits:
                cpu: 100.0m
                memory: 500Mi
          - args:
            - -cmd=nslookup
            - kubernetes.default.svc.cluster.local
            - 127.0.0.1
            - '>/dev/null'
            - -port=8080
            image: gcr.io/google_containers/exechealthz:1.0
            name: healthz
            ports:
            - containerPort: 8080
              protocol: TCP
            resources:
              limits:
                cpu: 10.0m
                memory: 20Mi
          - args:
            - --kubecfg-file=/etc/kubernetes/worker-kubeconfig.yaml
            - --domain=cluster.local
            image: gcr.io/google_containers/kube2sky:1.14
            name: kube2sky
            resources:
              limits:
                cpu: 100.0m
                memory: 200Mi
            volumeMounts:
            - mountPath: /etc/ssl/certs
              name: usr-share-ca-certificates
            - mountPath: /etc/kubernetes/worker-kubeconfig.yaml
              name: etc-kubernetes-worker-kubeconfig.yaml
              readOnly: true
            - mountPath: /etc/kubernetes/ssl
              name: etc-kubernetes-ssl
              readOnly: true
          - args:
            - -machines=http://127.0.0.1:4001
            - -addr=0.0.0.0:53
            - -ns-rotate=false
            - -domain=cluster.local.
            image: gcr.io/google_containers/skydns:2015-10-13-8c72f8c
            name: skydns
            ports:
            - containerPort: 53
              protocol: UDP
            - containerPort: 53
              protocol: TCP
            resources:
              limits:
                cpu: 100.0m
                memory: 200Mi
          volumes:
          - hostPath:
              path: /etc/kubernetes/ssl
            name: etc-kubernetes-ssl
          - hostPath:
              path: /etc/kubernetes/worker-kubeconfig.yaml
            name: etc-kubernetes-worker-kubeconfig.yaml
          - hostPath:
              path: /usr/share/ca-certificates
            name: usr-share-ca-certificates

Compose to ECS
~~~~~~~~~~~~~~

::

    $ cat docker-compose.yml | container-transform  -v
    {
        "family": "python-app",
        "volumes": [
            {
                "name": "host_logs",
                "host": {
                    "sourcePath": "/var/log/myapp"
                }
            }
        ],
        "containerDefinitions": [
            {
                "memory": 1024,
                "image": "postgres:9.3",
                "name": "db",
                "essential": true
            },
            {
                "memory": 128,
                "image": "redis:latest",
                "name": "redis",
                "essential": true
            },
            {
                "name": "web",
                "memory": 64,
                "command": [
                    "uwsgi",
                    "--json",
                    "uwsgi.json"
                ],
                "mountPoints": [
                    {
                        "sourceVolume": "host_logs",
                        "containerPath": "/var/log/uwsgi/"
                    }
                ],
                "environment": [
                    {
                        "name": "AWS_ACCESS_KEY_ID",
                        "value": "AAAAAAAAAAAAAAAAAAAA"
                    },
                    {
                        "name": "AWS_SECRET_ACCESS_KEY",
                        "value": "1111111111111111111111111111111111111111"
                    }
                ],
                "essential": true
            }
        ]
    }
    Container web is missing required parameter "image".
    Container web is missing required parameter "cpu".

Quick Help
----------
::

    Usage: container-transform [OPTIONS] [INPUT_FILE]

      container-transform is a small utility to transform various docker
      container formats to one another.

      Default input type is compose, default output type is ECS

      Default is to read from STDIN if no INPUT_FILE is provided

      All options may be set by environment variables with the prefix "CT_"
      followed by the full argument name.

    Options:
      -i, --input-type [ecs|compose|marathon|chronos|kubernetes]
      -o, --output-type [ecs|compose|systemd|marathon|chronos|kubernetes]
      -v, --verbose / --no-verbose    Expand/minify json output
      -q, --quiet                     Silence error messages
      --version                       Show the version and exit.
      -h, --help                      Show this message and exit.

Docker Image
------------

To get the docker image, run::

    docker pull micahhausler/container-transform:latest

To run the docker image::

    docker run --rm -v $(pwd):/data/ micahhausler/container-transform  docker-compose.yml

    # or
    cat docker-compose.yml | docker run --rm -i micahhausler/container-transform


Installation
------------

To install the latest release (Python 3 only), type::

    pip install container-transform

To install the latest code directly from source, type::

    pip install git+git://github.com/micahhausler/container-transform.git

Documentation
-------------

Full documentation is available at http://container-transform.readthedocs.org

License
-------
MIT License (see LICENSE)
