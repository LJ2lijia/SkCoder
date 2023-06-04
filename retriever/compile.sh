#!/bin/bash
javac -cp 'lucene-analyzers-common.jar:lucene-demo.jar:lucene.jar:lucene-queryparser.jar:.' IndexBuilder.java
javac -cp 'lucene-analyzers-common.jar:lucene-demo.jar:lucene.jar:lucene-queryparser.jar:.' Searcher.java
