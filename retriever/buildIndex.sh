#!/bin/bash
CLASSPATH='lucene-analyzers-common.jar:lucene-demo.jar:lucene.jar:lucene-queryparser.jar:.'

mkdir hs_corpus
java -cp $CLASSPATH IndexBuilder ../data/hearthstone/train.in hs_corpus

mkdir magic_corpus
java -cp $CLASSPATH IndexBuilder ../data/magic/train.in magic_corpus

