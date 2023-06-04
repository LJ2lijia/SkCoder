#!/bin/bash


mkdir hs_example_ids
./search.sh hs_corpus ../data/hearthstone/train.in hs_example_ids/train.example
./search.sh hs_corpus ../data/hearthstone/dev.in hs_example_ids/dev.example
./search.sh hs_corpus ../data/hearthstone/test.in hs_example_ids/test.example
mkdir magic_example_ids
./search.sh hs_corpus ../data/magic/train.in magic_example_ids/train.example
./search.sh hs_corpus ../data/magic/dev.in magic_example_ids/dev.example
./search.sh hs_corpus ../data/magic/test.in magic_example_ids/test.example