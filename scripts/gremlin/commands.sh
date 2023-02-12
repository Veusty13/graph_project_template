#!/bin/sh

grep -q gremlin.tinkergraph.vertexIdManager= conf/tinkergraph-empty.properties \
    && sed -i 's/gremlin.tinkergraph.vertexIdManager=.*/gremlin.tinkergraph.vertexIdManager=ANY/' conf/tinkergraph-empty.properties \
        || echo "gremlin.tinkergraph.vertexIdManager=ANY" >> conf/tinkergraph-empty.properties