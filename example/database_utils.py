import json

# from example.models import House, Student, Staff


def load_from_raw(
    house_data_file='example/raw_data/houses.json',
    student_data_file='example/raw_data/students.json',
    staff_data_file='example/raw_data/hogwarts_staff.json',
):
    from example.models import House, Student, Staff
    houses_map = dict()
    student_models = list()
    staff_models = list()

    with open(house_data_file, 'rt') as file:
        houses = json.load(file)
        for house in houses:
            houses_map[house['name']] = House(
                name=house['name'],
                location=house['location'],
                founder=house['founder'],
                colors=house['colors'],
                crest=house['crest'],
                ghost=house['ghost'],
            )

    with open(student_data_file, 'rt') as file:
        students = json.load(file)
        for student in students:
            student_models.append(
                Student(
                    name=student['name'],
                    house=houses_map[student['house']],
                    wand_wood=student['wand_wood'],
                    wand_core=student['wand_core'],
                    wand_length=float(student['wand_length']),
                ))

    with open(staff_data_file, 'rt') as file:
        staff = json.load(file)
        for staff_member in staff:
            staff_models.append(
                Staff(
                    name=staff_member['name'],
                    position=staff_member['position'],
                    specialization=staff_member['specialization'],
                    house=houses_map.get(staff_member.get('house')),
                    wand_wood=staff_member['wand_wood'],
                    wand_core=staff_member['wand_core'],
                    wand_length=float(staff_member['wand_length']),
                    wand=staff_member.get('wand'),
                ))

    print(houses_map)
    return list(houses_map.values()), student_models, staff_models
