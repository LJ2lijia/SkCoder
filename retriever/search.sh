#!/bin/bash
CLASSPATH='lucene-analyzers-common.jar:lucene-demo.jar:lucene.jar:lucene-queryparser.jar:.'
java -cp $CLASSPATH Searcher "$@"
