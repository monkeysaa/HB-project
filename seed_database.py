"""Script to seed database."""
import os
import json
from random import choice, randint

import crud
from model import *
import server

os.system('dropdb lessons')
os.system('createdb lessons')
connect_to_db(server.app, echo=False)
db.create_all()

# Load lesson data from JSON file
with open('static/data/lessons.json') as f:
    lesson_data = json.loads(f.read())

# Create users, store them in list so we can assign fake lessons to them
users_in_db = []
for n in range(3):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'
    # create a user here
    user = crud.create_user(email, password)
    users_in_db.append(user)

# Load component data from JSON file
with open('static/data/components.json') as f:
    comp_data = json.loads(f.read())

# Create components, store them in list so we can use them
# to create fake lesson components later
comps_in_db = []
for comp in comp_data:
    #unpack each component in comp_data from json file
    name, comp_type, url = (comp['name'],
                            comp['comp_type'],
                            comp['url'])

    # create a component and append it to comps_in_db
    db_comp = crud.create_comp(name, comp_type, url)
    comps_in_db.append(db_comp)

# Create fake tags, store them in a list so we can assign them later...
tags_in_db = []
tags = {
    'early_grades': ['Pre-K', 'K', '1st', '2nd', '3rd'],
    'subjects': ['Math', 'Writing', 'Reading', 'Science', 'Social Studies', 
                'Foreign Lang.', 'Arts/Music', 'Other']
}

for category, tags in tags.items():
        for tag in tags:
            tag = crud.create_tag(tag, category)
            tags_in_db.append(tag)

for n in range(4, 13):
    tag = crud.create_tag(f'{n}th', 'grade')
    tags_in_db.append(tag)


# Create fake lessons, store them in a list so we can assign fake components...
lessons_in_db = []
for lesson in lesson_data:
    #unpack each lesson in lesson data from json file
    title, description, public = (lesson['title'], lesson['description'], lesson['public'])

    # choose an author at random
    user = choice(users_in_db) 

    # create a lesson and append it to lessons_in_db
    db_lesson = crud.create_lesson(title, description, user.user_id, public)
    lessons_in_db.append(db_lesson)

    # assign components to lessons by hard-coding
    if db_lesson.title == 'Wolves':
            crud.assign_comp(comps_in_db[0], db_lesson)
            crud.assign_comp(comps_in_db[1], db_lesson)
            crud.assign_comp(comps_in_db[2], db_lesson)
            tag = crud.get_tag_by_name('Science')
            crud.assign_tag_to_lesson(tag, db_lesson)

    elif db_lesson.title == 'Multiplying fractions':
            crud.assign_comp(comps_in_db[3], db_lesson)
            crud.assign_comp(comps_in_db[4], db_lesson)
            crud.assign_comp(comps_in_db[5], db_lesson)
            tag = crud.get_tag_by_name('Math')
            crud.assign_tag_to_lesson(tag, db_lesson)

    elif db_lesson.title == 'Trophic cascades':
            crud.assign_comp(comps_in_db[0], db_lesson)
            crud.assign_comp(comps_in_db[6], db_lesson)
            crud.assign_comp(comps_in_db[7], db_lesson)
            tag = crud.get_tag_by_name('Science')
            crud.assign_tag_to_lesson(tag, db_lesson)

    elif db_lesson.title == 'Call to action intro':
            crud.assign_comp(comps_in_db[8], db_lesson)
            crud.assign_comp(comps_in_db[9], db_lesson)
            tag = crud.get_tag_by_name('Writing')
            crud.assign_tag_to_lesson(tag, db_lesson)

    





