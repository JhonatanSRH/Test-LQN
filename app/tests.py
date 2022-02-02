import json

from graphene_django.utils.testing import GraphQLTestCase

from swapi.schema import schema


class FirstTestCase(GraphQLTestCase):
    fixtures = ['app/fixtures/unittest.json']
    GRAPHQL_SCHEMA = schema

    def test_people_query(self):
        response = self.query(
            '''
            query {
                allPeople{
                    edges{
                        node{
                            name
                        }
                    }
                }
            }
            ''',
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertEqual(len(content['data']['allPeople']['edges']), 87)

    def test_people_mutation(self):
        add_response = self.query(
            '''
                mutation{
                    addPeople(input:{name: "Kylo Ren", gender: MALE, height: "189", mass: "89", hairColor: "black", eyeColor: "brown", skinColor: "light", birthYear: "5ABY", homeWorldId: 32}){
                        people{
                            id,
                            name,
                            gender,
                            height,
                            mass,
                            hairColor,
                            eyeColor,
                            skinColor,
                            birthYear
                            homeWorld{
                                name,
                            }
                        }
                    }
                }
            ''',
        )
        # Creacion correcta del Personaje
        self.assertResponseNoErrors(add_response)

        add_content = json.loads(add_response.content)
        add_expected_result = {'id': 'UGVvcGxlTm9kZTo4OQ==', 'name': 'Kylo Ren', 'gender': 'male', 'height': '189',
                               'mass': '89', 'hairColor': 'black', 'eyeColor': 'brown', 'skinColor': 'light',
                               'birthYear': '5ABY', 'homeWorld': {'name': 'Chandrila'}}
        # Prueba que la informacion se guardo con una estructura correcta
        self.assertEqual(add_content['data']['addPeople']['people'], add_expected_result)

        udpdate_response = self.query(
            '''
                mutation{
                    addPeople(input:{id: "UGVvcGxlTm9kZTo4OQ==", name: "Kylo Ren (Ben Solo)", homeWorldId: 32}){
                        people{
                            id,
                            name,
                            gender,
                            height,
                            mass,
                            hairColor,
                            eyeColor,
                            skinColor,
                            birthYear
                            homeWorld{
                                name,
                            }
                        }
                    }
                }
            ''',
        )
        # Comprueba que se haya actualizado el dato adecuadamente
        self.assertResponseNoErrors(add_response)

        update_content = json.loads(udpdate_response.content)
        update_expected_result = {'id': 'UGVvcGxlTm9kZTo4OQ==', 'name': 'Kylo Ren (Ben Solo)', 'gender': 'male',
                                  'height': '189', 'mass': '89', 'hairColor': 'black', 'eyeColor': 'brown',
                                  'skinColor': 'light', 'birthYear': '5ABY', 'homeWorld': {'name': 'Chandrila'}}
        # Comprueba lo que se actualizo, para que sea lo esperado
        self.assertEqual(update_content['data']['addPeople']['people'], update_expected_result)
