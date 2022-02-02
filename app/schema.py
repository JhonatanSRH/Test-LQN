import graphene
from django.db.models import Q
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id

from .models import Planet, People, Film, Director, Producer, GenderEnum
from .utils import generic_model_mutation_process

GenderEnumSchema = graphene.Enum.from_enum(GenderEnum)

class PlanetNode(DjangoObjectType):
    class Meta:
        model = Planet
        interfaces = (graphene.relay.Node,)
        filter_fields = {'name': ['iexact', 'icontains', 'contains', 'exact'], }


class AddPlanet(graphene.relay.ClientIDMutation):
    """Agrega un Planet model"""
    class Input:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)
        rotation_period = graphene.String(required=False)
        orbital_period = graphene.String(required=False)
        diameter = graphene.String(required=False)
        climate = graphene.String(required=False)
        gravity = graphene.String(required=False)
        terrain = graphene.String(required=False)
        surface_water = graphene.String(required=False)
        population = graphene.String(required=False)

    planet = graphene.Field(PlanetNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, **kwargs):
        # TODO: Por que args es None?
        # Inicialmente es el root de mutate_and_get_payload en el parametro de ClientIDMutation, 
        # dado que el metodo mutate_and_get_payload se trata como un metodo de clase el args / root equivale al cls
        # definido en la clase padre ClientIDMutation
        # TODO: Para que sirve el context?
        # context : Es un objeto que pasa el resolvedor de metodos  de graphene-django
        # kwargs recibe toda la data que se envia desde el mutation
        raw_id = kwargs.get('id', None)
        kw = {'model': Planet, 'data': kwargs}
        if raw_id:
            kw['id'] = from_global_id(raw_id)[1]
        planet = generic_model_mutation_process(**kw)
        return AddPlanet(planet=planet)


class PeopleNode(DjangoObjectType):
    class Meta:
        model = People
        interfaces = (graphene.relay.Node,)
        filter_fields = {'name': ['iexact', 'icontains', 'contains', 'exact'],
                         'gender': ['iexact', 'icontains', 'contains', 'exact'],
                         'hair_color': ['iexact', 'icontains', 'contains', 'exact'],}
        #convert_choices_to_enum = ['hair_color', 'eye_color', 'gender']
        convert_choices_to_enum = False


class AddPeople(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)
        height = graphene.String(required=False)
        mass = graphene.String(required=False)
        hair_color = graphene.String(required=False)
        skin_color = graphene.String(required=False)
        eye_color = graphene.String(required=False)
        birth_year = graphene.String(required=False)
        #gender = graphene.String(required=False)
        gender = GenderEnumSchema()

        home_world_id = graphene.ID(required=True)

    people = graphene.Field(PeopleNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, **kwargs):
        raw_id = kwargs.get('id', None)

        kw = {'model': People, 'data': kwargs}
        # Permite actualizar la informacion cuando se entrega un id concreto
        if raw_id:
            kw['id'] = from_global_id(raw_id)[1]
            people = generic_model_mutation_process(commit=True, **kw)
        else:
            people = generic_model_mutation_process(**kw)
        return AddPeople(people=people)


class DirectorNode(DjangoObjectType):
    class Meta:
        model = Director
        interfaces = (graphene.relay.Node,)
        filter_fields = ['name']


class AddDirector(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)

    director = graphene.Field(DirectorNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, **kwargs):
        raw_id = kwargs.get('id', None)

        kw = {'model': Director, 'data': kwargs}
        if raw_id:
            kw['id'] = from_global_id(raw_id)[1]
        director = generic_model_mutation_process(**kw)
        return AddDirector(director=director)


class ProducerNode(DjangoObjectType):
    class Meta:
        model = Producer
        interfaces = (graphene.relay.Node,)
        filter_fields = ['name']


class AddProducer(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)

    producer = graphene.Field(ProducerNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, **kwargs):
        raw_id = kwargs.get('id', None)

        kw = {'model': Producer, 'data': kwargs}
        if raw_id:
            kw['id'] = from_global_id(raw_id)[1]
        producer = generic_model_mutation_process(**kw)
        return AddProducer(producer=producer)


class ProducerInput(graphene.InputObjectType):
    """ Esto se puede utilizar dentro del class Input del AddProducer """

    class Meta:
        model = Producer

    id = graphene.ID()
    name = graphene.String()


class FilmNode(DjangoObjectType):
    class Meta:
        model = Film
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'title': ['iexact', 'icontains', 'contains', 'exact'],
            'episode_id': ['exact'],
            'release_date': ['exact']
        }

class PeopleInput(graphene.InputObjectType):
    """ Esto se puede utilizar dentro del class Input del AddProducer """

    class Meta:
        model = People

    id = graphene.ID()
    name = graphene.String()

class AddFilm(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=False)
        title = graphene.String(required=True)
        episode_id = graphene.Int(required=True)
        opening_crawl = graphene.String(required=False)
        release_date = graphene.Date()
        director = graphene.ID(required=False)
        producer = graphene.List(of_type=ProducerInput, required=False)
        character = graphene.List(of_type=PeopleInput, required=False)

    film = graphene.Field(FilmNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, **kwargs):
        raw_id = kwargs.get('id', None)

        # TODO: trabajar con el id de graphene.
        #director_id = kwargs.pop('director')
        director_id = from_global_id(kwargs.pop('director'))[1]
        
        producers = kwargs.pop('producer')
        
        characters = kwargs.pop('character')

        kw = {'model': Film, 'data': kwargs}
        if raw_id:
            kw['id'] = from_global_id(raw_id)[1]
        film = generic_model_mutation_process(commit=False, **kw)

        if director_id:
            film.director_id = director_id

        film.save()

        if producers:
            q = Q()
            for producer_name in producers:
                q |= Q(name__iexact=producer_name['name'])
            producer_instances = [producer for producer in Producer.objects.filter(q)]
            film.producer.set(producer_instances)

        if characters:
            q = Q()
            for character_name in characters:
                q |= Q(name__iexact=character_name['name'])
            character_instances = [character for character in People.objects.filter(q)]
            film.characters.set(character_instances)
        return AddFilm(film=film)


class Query(graphene.ObjectType):
    planet = graphene.relay.Node.Field(PlanetNode)
    all_planets = DjangoFilterConnectionField(PlanetNode)

    people = graphene.relay.Node.Field(PeopleNode)
    all_people = DjangoFilterConnectionField(PeopleNode)

    film = graphene.relay.Node.Field(FilmNode)
    all_films = DjangoFilterConnectionField(FilmNode)

    director = graphene.relay.Node.Field(DirectorNode)
    all_directors = DjangoFilterConnectionField(DirectorNode)

    producer = graphene.relay.Node.Field(ProducerNode)
    all_producers = DjangoFilterConnectionField(ProducerNode)


class Mutation(graphene.ObjectType):
    add_planet = AddPlanet.Field()  # TODO: debería tener 1 para add y otro para update?
    # Gracias al metodo generic_model_mutation_process dentro de las mutaciones, se puede crear o actualizar
    # Los modelos pasados en la mutacion, siempre y cuando se le envie un commit=True al llamar a la funcion.

    add_director = AddDirector.Field()

    add_producer = AddProducer.Field()

    add_people = AddPeople.Field()

    add_film = AddFilm.Field()
