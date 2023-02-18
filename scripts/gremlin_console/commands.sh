#!/bin/sh

grep -q hosts conf/remote.yaml \
    && sed -i 's/hosts.*/hosts: [graph-project-gremlin]/' conf/remote.yaml \
        || echo "hosts: [graph-project-gremlin]" >> conf/remote.yaml