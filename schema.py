import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType, utils
from graphql import GraphQLError

from models import House as HouseModel
from models import Student as StudentModel
from models import Pet as PetModel

from database import db_session


class HouseNode(SQLAlchemyObjectType):
	class Meta:
		model = HouseModel
		interfaces = (relay.Node, )


class HouseConnection(relay.Connection):
	class Meta:
		node = HouseNode


class StudentNode(SQLAlchemyObjectType):
	class Meta:
		model = StudentModel
		interfaces = (relay.Node, )


class StudentConnection(relay.Connection):
	class Meta:
		node = StudentNode


class PetNode(SQLAlchemyObjectType):
	class Meta:
		model = PetModel
		interfaces = (relay.Node, )


class PetConnection(relay.Connection):
	class Meta:
		node = PetNode

class CreatePet(relay.ClientIDMutation):
#class CreatePet(graphene.Mutation):
	class Input:
		name = graphene.String(required=True)
		species = graphene.String(required=True)
		student_name = graphene.String(required=True)

	pet = graphene.Field(PetNode)

	@classmethod
	def mutate_and_get_payload(cls, root, info, **input):
		query = StudentNode.get_query(info)
		student = query.filter(StudentModel.name == input['student_name']).first()
		pet = PetModel(name=input['name'],
			           species=input['species'],
			           student=student)

		db_session.add(pet)
		db_session.commit()

		return CreatePet(pet=pet)


class ChangeStudentHouse(relay.ClientIDMutation):
	class Input:
		name = graphene.String(required=True)
		house = graphene.String(required=True)

	student = graphene.Field(StudentNode)

	@classmethod
	def mutate_and_get_payload(cls, root, info, **input):
		student_query = StudentNode.get_query(info)
		student = student_query.filter(StudentModel.name == input['name']).first()
		house_query = HouseNode.get_query(info)
		house = house_query.filter(HouseModel.name == input['house']).first()

		student.house = house
		db_session.commit()

		return ChangeStudentHouse(student=student)


class Query(graphene.ObjectType):
	node = relay.Node.Field()
	
	# all data in table
	# set sort=None argument to disable ability to sort
	# all_houses = SQLAlchemyConnectionField(HouseConnection, sort=None)
	all_houses = SQLAlchemyConnectionField(HouseConnection)
	all_students = SQLAlchemyConnectionField(StudentConnection)
	all_pets = SQLAlchemyConnectionField(PetConnection)

	# custom filters
	student_by_name = graphene.Field(StudentNode, name=graphene.String())
	pet = graphene.Field(PetNode, name=graphene.String())
	pet_by_student_name = graphene.Field(PetNode, student_name=graphene.String())

	# simple resolver
	def resolve_student_by_name(self, info, name):
		query = StudentNode.get_query(info)
		if not name:
			raise GraphQLError("Please provide student name.")
		return query.filter(StudentModel.name == name).first()

	def resolve_pet(self, info, name):
		query = PetNode.get_query(info)
		if not name:
			raise GraphQLError("Please provide pet name.")
		return query.filter(PetModel.name == name).first()

	# traversing relationship between pet and student
	def resolve_pet_by_student_name(self, info, student_name):
		student_query = StudentNode.get_query(info)
		pet_query = PetNode.get_query(info)
		if not student_name:
			raise GraphQLError("Please provide student name.")
		student_result = student_query.filter(StudentModel.name == student_name).first()
		return pet_query.filter(PetModel.student_id == student_result.id).first()

class Mutation(graphene.ObjectType):
	create_pet = CreatePet.Field()
	change_student_house = ChangeStudentHouse.Field()


schema = graphene.Schema(query=Query, types=[HouseNode, StudentNode, PetNode], mutation=Mutation)
