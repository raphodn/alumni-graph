from py2neo import authenticate, Graph, Node, Relationship
from passlib.hash import bcrypt
import os

authenticate("localhost:7474", "neo4j", "shanghai")

#graph = Graph(os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474') + '/db/data/')
graph = Graph("http://localhost:7474/db/data/")


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


    def set_password(self, password):
        self.password = bcrypt.encrypt(password)
        return self

    def register(self):
        if not self.find():
            user = Node("User", username=self.username, password=self.password)
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_post(self, title, tags, text):
        import uuid

        user = self.find()
        post = Node(
            "Post",
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp=timestamp(),
            date=date()
        )
        rel = Relationship(user, "PUBLISHED", post)
        graph.create(rel)

        tags = [x.strip() for x in tags.lower().split(',')]
        for t in tags:
            tag = graph.merge_one("Tag", "name", t)
            rel = Relationship(tag, "TAGGED", post)
            graph.create(rel)

    def like_post(self, post_id):
        user = self.find()
        post = graph.find_one("Post", "id", post_id)
        graph.create_unique(Relationship(user, "LIKED", post))

    def get_similar_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = """
        MATCH (you:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (they:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE you.username = {username} AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags, COUNT(DISTINCT tag) AS len
        ORDER BY len DESC LIMIT 3
        RETURN they.username AS similar_user, tags
        """

        similar = graph.cypher.execute(query, username=self.username)
        return similar

    def get_commonality_of_user(self, username):
        # Find how many of the logged-in user's posts the other user
        # has liked and which tags they've both blogged about.
        query = """
        MATCH (they:User {username:{they}}),
              (you:User {username:{you}})
        OPTIONAL MATCH (they)-[:LIKED]->(post:Post)<-[:PUBLISHED]-(you)
        OPTIONAL MATCH (they)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
                       (you)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        RETURN COUNT(DISTINCT post) AS likes, COLLECT(DISTINCT tag.name) AS tags
        """

        result = graph.cypher.execute(query,
                                      they=username,
                                      you=self.username)

        result = result[0]
        common = dict()
        common['likes'] = result.likes
        common['tags'] = result.tags if len(result.tags) > 0 else None
        return common




## Various functions.
## These are for the views.



def find_node_label(node):
    labels = []
    for label in node.labels:
        labels.append(label)
    return labels[0] # suppose every node has only 1 label






def node_recordlist_to_array(all_nodes):
    """
    all_nodes: RecordList
    node in all_nodes:
        node: Record (or Node ??)
        node[0].labels: LabelSet
        node[0].properties: PropertySet
        node[0]['name'] or node[0].properties['name']
    """
    array = []
    for node in all_nodes:
        array.append(find_node_label(node[0]))
        array.append(node[0].properties)
    return array


def relationship_to_array(rel):
    """
    all_relationships: (iterator)
    rel in all_relationships:
        rel: ()
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
    return array



def get_all_nodes(nodes):
    if (nodes == 'All'):
        query = "MATCH (n) RETURN n"
        all_nodes = graph.cypher.execute(query) #graph.cypher.execute("MATCH (p:Person), (s:School) RETURN p.first_name, s:name")

    if (nodes == 'School'):
        query = "MATCH (school:School) RETURN school"
        all_nodes = graph.cypher.execute(query)
    
    node_data = node_recordlist_to_array(all_nodes)
    
    return node_data


def get_all_relationships():
    all_relationships = graph.match() #graph.cypher.execute("MATCH (n)-[r]->() RETURN r")
    
    rel_data = []
    
    for rel in all_relationships:
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