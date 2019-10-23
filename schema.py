import graphene as gp
import graphene_sqlalchemy as gp_sa
import graphql as gq
import graphql_relay as gq_relay
from pprint import pprint

from models import House as HouseModel
from models import Student as StudentModel
from models import Staff as StaffModel

import database as db

class HouseNode(gp_sa.SQLAlchemyObjectType):
	class Meta:
		model = HouseModel
		interfaces = (gp.relay.Node, )

class HouseConnection(gp.relay.Connection):
	class Meta:
		node = HouseNode

class StudentNode(gp_sa.SQLAlchemyObjectType):
	class Meta:
		model = StudentModel
		interfaces = (gp.relay.Node, )

class StudentConnection(gp.relay.Connection):
	class Meta:
		node = StudentNode

class StaffNode(gp_sa.SQLAlchemyObjectType):
	class Meta:
		model = StaffModel
		interfaces = (gp.relay.Node, )

	teacher = gp.String(description="A Hogwarts teacher.",
		                deprecation_reason="Replaced with staff.")
	wand = gp.String(description="String that describes wand.",
					 deprecation_reason="Use wand_wood, wand_core, wand_length "
					                    "and optionally wand_unit (default inches) "
										"to describe a wand instead.")

class StaffConnection(gp.relay.Connection):
	class Meta:
		node = StaffNode

class SearchResult(gp.Union):
    class Meta:
        types = (StaffNode, StudentNode)


# # TODO: add pet only through student mutation?
# # class CreatePet(gp.relay.ClientIDMutation):
# # 	class Input:
# # 		name = gp.String(required=True)
# # 		species = gp.String(required=True)
# # 		# student_name = gp.String(required=True)

# # 	pet = gp.Field(PetNode)
# # 	ok = gp.Boolean()

# # 	@classmethod
# # 	def mutate_and_get_payload(cls, root, info, pet_name, pet_species, id):
# # 		print(from_global_id(id))
# # # 		query = StudentNode.get_query(info)
# # # 		# student_query = StudentNode.get_query(info)
# # # 		if not input['name']:
# # # 			raise gq.GraphQLError('Please provide pet name.')
# # # 		if not input['species']:
# # # 			raise gq.GraphQLError('Please provide pet species.')
# # # 		# if not input['student_name']:
# # # 		# 	raise gq.GraphQLError('Please provide student name.')

# # # 		# student = query.filter(StudentModel.name == input['student_name']).first()
# # # 		# if not student:
# # # 		# 	raise gq.GraphQLError(f'Could not find student {input["student_name"]}')

# # 		# pet = PetModel(name=input['name'],
# # 		# 	           species=input['species'],
# # 		# 	           student=student)
# # 		pet = PetModel(name=input['name'],
# # 			           species=input['species'])

# # 		db.db_session.add(pet)
# # 		db.db_session.commit()
# # 		ok = True

# # 		return CreatePet(pet=pet, ok=ok)


# class ChangeStudentHouse(gp.relay.ClientIDMutation):
# 	class Input:
# 		name = graphene.String(required=True)
# 		house = graphene.String(required=True)

# 	student = graphene.Field(StudentNode)
# 	ok = graphene.Boolean()

# 	@classmethod
# 	def mutate_and_get_payload(cls, root, info, student_name, house_name, id):
# 		print(from_global_id(id))
# # 		student_query = StudentNode.get_query(info)
# # 		if not input['name']:
# # 			raise gq.GraphQLError('Please provide student name.')
# # 		if not input['house']:
# # 			raise gq.GraphQLError('Please provide student house.')
	
# # 		student = student_query.filter(StudentModel.name == input['name']).first()
# # 		if not student:
# # 			raise gq.GraphQLError(f'Could not find student {input["name"]}')
	
# # 		house_query = HouseNode.get_query(info)
# # 		house = house_query.filter(HouseModel.name == input['house']).first()
# # 		if not house:
# # 			raise gq.GraphQLError(f'Could not find house {input["house"]}')
# # 		student.house = house
# # 		db.db_session.commit()
# # 		ok = True
# # 		return ChangeStudentHouse(student=student, ok=ok)

class CreateStudent(gp.relay.ClientIDMutation):
	class Input:
		name = gp.String(required=True)
		id = gp.ID()
		# etc.

	student = gp.Field(StudentNode)
	success = gp.Boolean()

	@classmethod
	# def mutate_and_get_payload(cls, root, info, name, wand_wood, wand_core, wand_length, wand_length_unit, house_name, id):
	def mutate_and_get_payload(cls, root, info, name, id):
		print(gq_relay.from_global_id(id))
		print(name)

		success = False
		return CreateStudent(student=None, success=success)


class ChangeStudentHouse(gp.relay.ClientIDMutation):
	class Input:
		name = gp.String(required=True)
		house = gp.String(required=True)
		id = gp.ID()

	student = gp.Field(StudentNode)
	success = gp.Boolean()

	@classmethod
	def mutate_and_get_payload(cls, root, info, name, house_name, id):
		# student_query = StudentNode.get_query(info)
		print(gq_relay.from_global_id(id))
		student_query = Student.objects.get(pk=gq_relay.from_global_id(id)[1])
		if not name:
			raise gq.GraphQLError('Please provide student name.')
		if not house_name:
			raise gq.GraphQLError('Please provide student house.')
	
		student = student_query.filter(StudentModel.name == name).first()
		if not student:
			raise gq.GraphQLError(f'Could not find student {name}')
	
		house_query = HouseNode.get_query(info)
		house = house_query.filter(HouseModel.name == house_name).first()
		if not house:
			raise gq.GraphQLError(f'Could not find house {house_name}')

		student.house = house
		db.db_session.commit()
		success = True

		return ChangeStudentHouse(student=student, success=success)


class Query(gp.ObjectType):
	node = gp.relay.Node.Field()
	
	# Default filters that return all data in table
	#
	# Set sort=None argument to disable ability to sort
	# For example:
	# all_houses = gp_sa.SQLAlchemyConnectionField(HouseConnection, sort=None)
	all_houses = gp_sa.SQLAlchemyConnectionField(HouseConnection)
	all_students = gp_sa.SQLAlchemyConnectionField(StudentConnection)
	all_staff = gp_sa.SQLAlchemyConnectionField(StaffConnection)

	# custom filters
	student_by_name = gp.Field(StudentNode, name=gp.String())
	staff_by_name = gp.Field(StaffNode, name=gp.String())
	house_by_name = gp.Field(HouseNode, name=gp.String())
	staff_by_position = gp.List(StaffNode, position=gp.String())
	search_by_house = gp.List(SearchResult, house_name=gp.String())

	# simple resolver
	def resolve_student_by_name(self, info, name):
		query = StudentNode.get_query(info)
		# for demonstration purposes
		pprint(str(query))
		if not name:
			raise gq.GraphQLError('Please provide student name.')
		return query.filter(StudentModel.name == name).first()

	def resolve_staff_by_name(self, info, name):
		query = StaffNode.get_query(info)
		if not name:
			raise gq.GraphQLError('Please provide staff member name.')
		return query.filter(StaffModel.name == name).first()
	
	def resolve_house_by_name(self, info, name):
		query = HouseNode.get_query(info)
		if not name:
			raise gq.GraphQLError('Please provide Hogwarts house name.')
		return query.filter(HouseModel.name == name).first()

	def resolve_staff_by_position(self, info, position):
		query = StaffNode.get_query(info)
		# for demonstration purposes
		pprint(str(query))
		if not position:
			raise gq.GraphQLError('Please provide staff position.')
		r = query.filter(StaffModel.position == position).all()
		return r

	def resolve_search_by_house(self, info, house_name):
		staff_query = StaffNode.get_query(info)
		student_query = StudentNode.get_query(info)
		house_query = HouseNode.get_query(info)
		if not house_name:
			raise gq.GraphQLError('Please provide house name.')

		house = house_query.filter(HouseModel.name == house_name).first()

		staff_results = staff_query.filter(StaffModel.house == house).all()
		student_results = student_query.filter(StudentModel.house == house).all()
		return staff_results + student_results


# 	# TODO: new traverse relationship!!!

# 	# # traversing relationship between pet and student
# 	# def resolve_pet_by_student_name(self, info, student_name):
# 	# 	student_query = StudentNode.get_query(info)
# 	# 	pet_query = PetNode.get_query(info)
# 	# 	if not student_name:
# 	# 		raise gq.GraphQLError('Please provide student name.')
# 	# 	student_result = student_query.filter(StudentModel.name == student_name).first()
# 	# 	return pet_query.filter(PetModel.student_id == student_result.id).first()

class Mutation(gp.ObjectType):
	create_student = CreateStudent.Field()
	change_student_house = ChangeStudentHouse.Field()


schema = gp.Schema(query=Query,
                   types=[HouseNode, StudentNode, StaffNode, SearchResult],
				   mutation=Mutation)