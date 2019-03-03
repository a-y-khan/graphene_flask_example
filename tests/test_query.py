import pytest

from graphene.test import Client
from schema import schema

# test example
# see https://docs.graphene-python.org/en/latest/testing/

def test_all_houses():
	client = Client(schema)
	query = '''
	{
	  allHouses {
	    edges {
	      node {
	        name
	      }
	    }
	  }
	}'''
	result = {
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
	assert executed == result