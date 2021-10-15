import pytest

from graphene.test import Client

from example.database import load_from_raw
from example.schema import schema

# test example
# see https://docs.graphene-python.org/en/latest/testing/


def add_test_data(session):
	house_models, student_models, staff_models = load_from_raw()
	for model in house_models + student_models + staff_models:
		session.add(model)
	session.commit()


def test_all_houses(session):
	add_test_data(session)
	client = Client(schema)
	query = """
	{
	  allHouses {
	    edges {
	      node {
	        name
	      }
	    }
	  }
	}"""
	expected_result = {
	  "data": {
	    "allHouses": {
	      "edges": [
	        {
	          "node": {
	            "name": "Gryffindor"
	          }
	        },
	        {
	          "node": {
	            "name": "Ravenclaw"
	          }
	        },
	        {
	          "node": {
	            "name": "Hufflepuff"
	          }
	        },
	        {
	          "node": {
	            "name": "Slytherin"
	          }
	        }
	      ]
	    }
	  }
	}

	executed = client.execute(query)
	print(executed)
	assert executed == expected_result