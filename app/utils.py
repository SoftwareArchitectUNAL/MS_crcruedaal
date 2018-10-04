from pymongo import MongoClient

def get_mongo_instance():
    
    # connection_str = 'mongodb://root:example@192.168.99.102:27017/analysis_data' docker
    connection_str = 'mongodb://admin:1234@localhost:27017/analysis_data'
    client = MongoClient(connection_str)
    return client
#eval $(docker-machine env rancher-node2)
