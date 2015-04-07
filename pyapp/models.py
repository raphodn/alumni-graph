from py2neo import authenticate, Graph, Node, Relationship
from passlib.hash import bcrypt
import os

authenticate("localhost:7474", "neo4j", "shanghai")

#graph = Graph(os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474') + '/db/data/')
graph = Graph("http://localhost:7474/db/data/")

"""
py2neo API

graph.find() ; graph.match()
    > RETURNS generator
    > elem in generator: Node or Relationship

graph.execute() > RETURNS RecordList
    > elem in RecordList: Record
    > elem[0]: Node


graph.find(label, property_key=None, property_value=None, limit=None)
graph.find_one(label, property_key=None, property_value=None)


"""


class Person:
    """
    - id (UNIQUE CONSTRAINT)
    - first_name
    - last_name
    - email
    - bio
    - link
    - privacy ?
    """
    def __init__(self, id=None):
        self.id = id

    def get_person(self):
        person = graph.find_one("Person", "id", self.id)
        if person:
            person_data = []
            person_data.append(node_to_array(person))
            return person_data
        else:
            return None

    def search_persons(self):
        """
        Privacy issues ?
        """
        search_persons = graph.cypher.execute("MATCH (person:Person) WHERE person.name =~ '(?i).*." + self.name + ".*' RETURN person")
        return node_recordlist_to_array(search_persons)

    def get_all_persons(self):
        all_persons = graph.find("Person")
        return nodelist_to_array(all_persons)

    def create(self, first_name, last_name):
        person = Node("Person", id=person_id, first_name=first_name, last_name=last_name)
        graph.create(person)
        return True



class School:
    """
    name (UNIQUE CONSTRAINT)
    """
    def __init__(self, name=None):
        self.name = name

    def get_school(self):
        school = graph.find_one("School", "name", self.name) # graph.cypher.execute_one("MATCH (school:School {name:{S}}) RETURN school.name", {"S": self.name})
        if school:
            school_data = []
            school_data.append(node_to_array(school))
            return school_data
        else:
            return None

    def search_schools(self):
        search_schools = graph.cypher.execute("MATCH (school:School) WHERE school.name =~ '(?i).*." + self.name + ".*' RETURN school")
        return node_recordlist_to_array(search_schools)

    def get_all_schools(self):
        all_schools = graph.find("School") # graph.cypher.execute_one("MATCH (school:School) RETURN school.name")
        return nodelist_to_array(all_schools)

    def create(self):
        if not self.get_school():
            school = Node("School", name=name)
            graph.create(school)
            return True
        else:
            return False



class Company:
    """
    name (UNIQUE CONSTRAINT), HQ address ?
    """
    def __init__(self, name=None):
        self.name = name

    def get_company(self):
        company = graph.find_one("Company", "name", self.name)
        if company:
            company_data = []
            company_data.append(node_to_array(company))
            return company_data
        else:
            return None

    def search_companies(self):
        search_companies = graph.cypher.execute("MATCH (company:Company) WHERE company.name =~ '(?i).*." + self.name + ".*' RETURN company")
        return node_recordlist_to_array(search_companies)

    def get_all_companies(self):
        all_companies = graph.find("Company")
        return nodelist_to_array(all_companies)

    def create(self):
        if not self.get_company():
            company = Node("Company", name=name)
            graph.create(company)
            return True
        else:
            return False





## Various functions.
## These are for the views.



def find_node_label(node):
    labels = []
    for label in node.labels:
        labels.append(label)
    return labels[0] # for now suppose every node has only 1 label



def node_to_array(node):
    """
    node: Node
    node.labels: LabelSet
    node.properties: PropertySet
    node['name'] or node.properties['name']
    """
    array = []
    
    array.append(find_node_label(node))
    array.append(node.properties)
    
    return array



def node_recordlist_to_array(recordlist):
    """
    recordlist: RecordList
    record in recordlist: Record
    record[0]: Node
    """
    array = []
    
    for record in recordlist:
        array.append(node_to_array(record[0]))
    
    return array


def nodelist_to_array(nodelist):
    """
    recordlist: RecordList
    record in recordlist: Record
    record[0]: Node
    """
    array = []
    
    for node in nodelist:
        array.append(node_to_array(node))
    
    return array



def relationship_to_array(rel):
    """
    rel: Relationship
    rel.start_node: Node
    rel.type: String
    rel.properties: PropertySet
    rel.end_node: Node
    """
    array = []
    
    array.append(rel.start_node.properties)
    array.append(rel.type)
    array.append(rel.properties)
    array.append(rel.end_node.properties)
    
    # [{start_node properties}, REL_TYPE, {rel properties}, {end_node properties}]
    return array



def get_all_nodes():
    query = "MATCH (n) RETURN n"
    all_nodes = graph.cypher.execute(query) #graph.cypher.execute("MATCH (p:Person), (s:School) RETURN p.first_name, s:name")
    return node_recordlist_to_array(all_nodes)


def get_all_relationships():
    all_relationships = graph.match() #graph.cypher.execute("MATCH (n)-[r]->() RETURN r")

    rel_data = []
    
    for rel in all_relationships:
        # all_relationships: (py2neo generator)
        # rel: Relationship
        rel_data.append(relationship_to_array(rel))
    
    return rel_data




def get_school(school_name):
    school = graph.cypher.execute_one("MATCH (school:School {name:{S}}) RETURN school.name", {"S": school_name})
    print(school)
    return school


def get_all_fields_from_school(school_name):
    all_fields_from_schools = graph.cypher.execute("MATCH (School { name:{S}})--(field:Field) RETURN field", {"S": school_name})
    return all_fields_from_schools


def get_all_years_from_school_field(school_name, field_name):
    all_years_from_school_field = graph.cypher.execute("MATCH (School { name:{S}})--(Field { name:{F}})--(year:Year) RETURN year", {"S": school_name, "F": field_name})
    return all_years_from_school_field


def get_all_alumni_from_school_field_year(school_name, field_name, year):
    all_years_from_school_field = graph.cypher.execute("MATCH (School { name:{S}})--(Field { name:{F}})--(Year {name:{Y}}) RETURN year", {"S": school_name, "F": field_name, "Y": year})
    return all_years_from_school_field











############################################################################################
# from https://github.com/nicolewhite/neo4j-flask
############################################################################################


## The User class.
## This class is for handling 
class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user

    def create(self, first_name, last_name):
        #if not self.find():
        user = Node("User", first_name=first_name, last_name=last_name)
        graph.create(user)
        return True
        #else:
            #return False


# For the profile/<username> view.
def get_users_recent_posts(username):
    query = """
    MATCH (:User {username:{username}})-[:PUBLISHED]->(post:Post),
          (tag:Tag)-[:TAGGED]->(post)
    RETURN post.id AS id,
           post.date AS date,
           post.timestamp AS timestamp,
           post.title AS title,
           post.text AS text,
           COLLECT(tag.name) AS tags
    ORDER BY timestamp DESC
    LIMIT 5
    """

    posts = graph.cypher.execute(query, username=username)
    return posts

# For the / view.
def get_todays_recent_posts():
    query = """
    MATCH (post:Post {date: {today}}),
          (user:User)-[:PUBLISHED]->(post),
          (tag:Tag)-[:TAGGED]->(post)
    RETURN user.username AS username,
           post.id AS id,
           post.date AS date,
           post.timestamp AS timestamp,
           post.title AS title,
           post.text AS text,
           COLLECT(tag.name) AS tags
    ORDER BY timestamp DESC
    LIMIT 5
    """

    posts = graph.cypher.execute(query, today = date())
    return posts

## Helper functions.
from datetime import datetime

def timestamp():
    unix = int(datetime.now().strftime('%s'))
    return unix

def date():
    today = datetime.now().strftime('%Y-%m-%d')
    return today