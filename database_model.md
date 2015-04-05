This document explains how data is organized within the graph database. **Nodes** are connected through typed, directed **Relationships**
Each single Node and Relationship can have named attributes referred to as **Properties**. A **Label** is a name that organizes nodes into groups.

The database contains time nodes managed by the GraphAware Framework that will not be explained here. However the relationships of our nodes towards time nodes are detailed. 

##Labels 
####Label *Person*
 - first_name
 - last_name
 - email
 - bio
 - link

####Label *University*
 - name

####Label *School*
 - name

####Label *Laboratory*
 - name

####Label *Company*
 - name

####Label *Studies*

 - name
 - description

####Label *Job*

 - name
 - description

##Relationships
####From *Person* to *Studies*
 - **STUDIED** : (:Person) - [:STUDIED] -> (:Studies)

####From *Person* to *Job*
 - **WORKED** : (:Person) - [:WORKED] -> (:Job)

####From *Person* to *Time*
 - **BORN** : (:Person) - [:BORN] -> (:Time)

####From *Studies*, *Job* to *University*, *School*, *Laboratory*, *Company*
 - **AT** : (Studies) - [:AT] -> (:University) 

####From *Studies*, *Job* to *Time*
 - **FROM** : (Studies) - [:FROM] -> [:TIME]
 - **TO** : (Studies) - [:TO] -> [:TIME]

####From *Lab* to *School* and from *School* to *University*
 - **BELONGS_TO** : (:School) - [:BELONGS_TO] -> (:University)
