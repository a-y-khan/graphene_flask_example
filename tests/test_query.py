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


def test_query_all_houses(session):
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
                "edges": [{
                    "node": {
                        "name": "Gryffindor"
                    }
                }, {
                    "node": {
                        "name": "Ravenclaw"
                    }
                }, {
                    "node": {
                        "name": "Hufflepuff"
                    }
                }, {
                    "node": {
                        "name": "Slytherin"
                    }
                }]
            }
        }
    }

    executed = client.execute(query)
    assert executed == expected_result


def test_query_house_by_name(session):
    add_test_data(session)
    client = Client(schema)
    query = """
		query($name: String!){
			houseByName(name: $name) {
				founder
				location
				colors
			}
		}
	"""
    expected_result = {
        'data': {
            'houseByName': {
                'founder': 'Rowena Ravenclaw',
                'location': 'Ravenclaw tower',
                'colors': 'blue, bronze'
            }
        }
    }
    executed = client.execute(query, variable_values={"name": "Ravenclaw"})
    assert executed == expected_result
