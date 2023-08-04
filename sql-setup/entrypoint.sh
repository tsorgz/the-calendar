#!/bin/bash

psql -d $POSTGRES_URL -f sql/schema_setup.sql