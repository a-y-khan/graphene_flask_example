from datetime import datetime
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
	"""Node to support House type."""
	class Meta:
		model = HouseModel
		interfaces = (gp.relay.Node, )

class HouseConnection(gp.relay.Connection):
	"""Connection to support listing House nodes."""
	# Meta is required
	class Meta:
		node = HouseNode
	
	# Edge, other fields like total_count and their resolvers
	# are optional
	class Edge:
		"""Annotate connection edges with additional fields."""
		timestamp = gp.String(description="Annotate edge with timestamp.")
		def resolve_timestamp(self, info):
			return datetime.now().isoformat()

	total_count = gp.Int(description="Count how many houses are in list.")

	def resolve_total_count(self, info):
		return HouseNode.get_query(info).count()

class StaffNode(gp_sa.SQLAlchemyObjectType):
	"""Node to support Staff type."""
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
	"""Connection to support listing Staff nodes."""
	class Meta:
		node = StaffNode

class StudentNode(gp_sa.SQLAlchemyObjectType):
	"""Node to support Student type."""
	# Meta is required
	class Meta:
		model = StudentModel
		interfaces = (gp.relay.Node, )

class StudentConnection(gp.relay.Connection):
	"""Connection to support listing Student nodes."""
	# Meta is required
	class Meta:
		node = StudentNode

	# Any additional fields like total_count and their resolvers are optional
	total_count = gp.Int(description="Count how many students are in list.")

	def resolve_total_count(self, info):
		return StudentNode.get_query(info).count()

class HouseEnrollment(gp.ObjectType):
	"""Get the students that were sorted into a house."""
	class Meta:
		interfaces = (gp.relay.Node, )

	students = gp_sa.SQLAlchemyConnectionField(
		StudentConnection,
		description="Students sorted into this house.")
	def resolve_students(self, info, **input):
		return self.students

	@classmethod
	def get_node(cls, info, id):
		return HouseEnrollment(id=id)

class SearchResult(gp.Union):
	"""Union of Staff and Student types."""
	class Meta:
		types = (StaffNode, StudentNode)

class CreateStudent(gp.relay.ClientIDMutation):
	"""Create a new Hogwarts student."""
	class Input:
		name = gp.String(required=True)
		house_name = gp.String(required=True)
		wand_wood = gp.String()
		wand_core = gp.String()
		wand_length = gp.Float()
		wand_length_unit = gp.String()

	student = gp.Field(StudentNode)
	success = gp.Boolean()

	@classmethod
	def mutate_and_get_payload(cls, root, info, **input):
		house_query = HouseNode.get_query(info)
		house = house_query.filter(HouseModel.name == input['house_name']).first()
		if not house:
			raise gq.GraphQLError(f'Could not find house with name {input["house_name"]}')

		student = StudentModel(name=input['name'],
		                       house=house,
							   wand_wood=input.get('wand_wood'),
							   wand_core=input.get('wand_core'),
							   wand_length=input.get('wand_length', 0),
							   wand_length_unit=input.get('wand_length_unit'))

		student_query = StudentNode.get_query(info)
		found_students = student_query.filter(
			(StudentModel.name == student.name) and
		    (StudentModel.house_id == student.house_id) and
			(StudentModel.wand_wood == student.wand_wood) and
			(StudentModel.wand_core == student.wand_core) and
			(StudentModel.wand_length == student.wand_length) and
			(StudentModel.wand_length_unit == student.wand_length_unit)).all()

		if len(found_students):
			for s in found_students:
				print(s.id)
			raise gq.GraphQLError(f'Student with attributes {input} already exists')

		db.db_session.add(student)
		db.db_session.commit()
		return CreateStudent(student=student, success=True)

class ChangeStudentHouse(gp.relay.ClientIDMutation):
	"""Assign a Hogwarts student to a new House."""
	class Input:
		house_name = gp.String(required=True)
		id = gp.ID(required=True)
	student = gp.Field(StudentNode)
	success = gp.Boolean()

	@classmethod
	def mutate_and_get_payload(cls, root, info, house_name, id,
	                           client_mutation_id=None):
		student_id = gq_relay.from_global_id(id)[1]
		student_query = StudentNode.get_query(info)
		student = student_query.filter(StudentModel.id == student_id).first()
		if not student:
			raise gq.GraphQLError(f'Could not find student with id {id}')

		house_query = HouseNode.get_query(info)
		house = house_query.filter(HouseModel.name == house_name).first()
		if not house:
			raise gq.GraphQLError(f'Could not find house {house_name}')
		student.house = house
		db.db_session.commit()
		return ChangeStudentHouse(student=student, success=True)

class DeleteStudent(gp.relay.ClientIDMutation):
	"""Delete a Hogwarts student's data."""
	class Input:
		id = gp.ID(required=True)

	student = gp.Field(StudentNode)
	success = gp.Boolean()

	@classmethod
	def mutate_and_get_payload(cls, root, info, id, client_mutation_id=None):
		student_id = gq_relay.from_global_id(id)[1]
		student_query = StudentNode.get_query(info)
		student = student_query.filter(StudentModel.id == student_id).first()
		if not student:
			raise gq.GraphQLError(f'Could not find student with id {id}')

		db.db_session.delete(student)
		db.db_session.commit()
		return DeleteStudent(student=student, success=True)

class Query(gp.ObjectType):
	# node root field required by Relay specification
	node = gp.relay.Node.Field()
	
	# Filters that return all data for types
	#
	# Set sort=None argument to disable ability to sort
	# For example:
	# all_houses = gp_sa.SQLAlchemyConnectionField(HouseConnection, sort=None)
	all_houses = gp_sa.SQLAlchemyConnectionField(
		HouseConnection,
	    description="Get all Hogwarts Houses.")
	all_students = gp_sa.SQLAlchemyConnectionField(
		StudentConnection,
		description="Get all students enrolled at Hogwarts.")
	all_staff = gp_sa.SQLAlchemyConnectionField(
		StaffConnection,
		description="Get all staff who work at Hogwarts.")

	# Targeted filters
	student_by_name = gp.Field(StudentNode, name=gp.String(),
	                           description="Get Hogwarts student by name.")
	staff_by_name = gp.Field(StaffNode, name=gp.String(),
	                         description="Get Hogwarts staff member by name.")
	house_by_name = gp.Field(HouseNode, name=gp.String(),
	                         description="Get Hogwarts House by name.")
	staff_by_position = gp.List(StaffNode, position=gp.String(),
	                            description="Get Hogwarts staff member by position.")
	search_by_house = gp.List(SearchResult, house_name=gp.String(),
	                          description="Get Hogwarts staff members and students "
							              "by house.")
	house_enrollment = gp.Field(HouseEnrollment, house_name=gp.String(),
	                            description="Get students sorted into a house.")

	# simple resolver	
	def resolve_house_by_name(self, info, name):
		query = HouseNode.get_query(info)
		if not name:
			raise gq.GraphQLError('Please provide Hogwarts house name')
		return query.filter(HouseModel.name == name).first()

	def resolve_student_by_name(self, info, name):
		query = StudentNode.get_query(info)
		if not name:
			raise gq.GraphQLError('Please provide student name')
		return query.filter(StudentModel.name == name).first()

	def resolve_staff_by_name(self, info, name):
		query = StaffNode.get_query(info)
		if not name:
			raise gq.GraphQLError('Please provide staff member name')
		return query.filter(StaffModel.name == name).first()

	def resolve_staff_by_position(self, info, position):
		query = StaffNode.get_query(info)
		# for demonstration purposes
		pprint(str(query))
		if not position:
			raise gq.GraphQLError('Please provide staff position')
		return query.filter(StaffModel.position == position).all()

	def resolve_search_by_house(self, info, house_name):
		staff_query = StaffNode.get_query(info)
		student_query = StudentNode.get_query(info)
		house_query = HouseNode.get_query(info)
		if not house_name:
			raise gq.GraphQLError('Please provide house name')

		house = house_query.filter(HouseModel.name == house_name).first()

		staff_results = staff_query.filter(StaffModel.house == house).all()
		student_results = student_query.filter(StudentModel.house == house).all()
		return staff_results + student_results
	
	def resolve_house_enrollment(self, info, house_name):
		house_query = HouseNode.get_query(info)
		house = house_query.filter(HouseModel.name == house_name).first()
		student_query = StudentNode.get_query(info)
		return HouseEnrollment(students=student_query.filter(
			StudentModel.house == house).all())

class Mutation(gp.ObjectType):
	create_student = CreateStudent.Field()
	change_student_house = ChangeStudentHouse.Field()
	delete_student = DeleteStudent.Field()

schema = gp.Schema(query=Query,
                   types=[HouseNode, StudentNode, StaffNode,
				          HouseEnrollment, SearchResult],
				   mutation=Mutation)