from pyArango.collection import Collection, Field, Edges
from pyArango.graph import Graph, EdgeDefinition


class players(Collection):
    _fields = {
        "username": Field()
    }


class questions(Collection):
    _fields = {
        "question": Field(),
        "answer": Field(),
        "wrong_answers": Field()

    }


class games(Collection):
    _fields = {
        "chat_id": Field(),
        "status": Field()
    }


class categories(Collection):
    _fields = {
        "name": Field()
    }


class played(Edges):
    _fields = {
        "score":Field()
    }


class answered(Edges):
    _fields = {
        "correct": Field()
    }


class contains(Edges):
    _fields = {
        "correct_answer_count":Field(),
        "wrong_answer_count":Field()
    }

class isOfCategory(Edges):
    _fields = {

    }

# Here's how you define a graph
class TriviaGraph(Graph):
    _edgeDefinitions = [EdgeDefinition("played", fromCollections=["players"], toCollections=["games"]),
                        EdgeDefinition("contains", fromCollections=["games"], toCollections=["questions"]),
                        EdgeDefinition("isOfCategory", fromCollections=["questions"], toCollections=["categories"]),
                        EdgeDefinition("answered", fromCollections=["players"], toCollections=["questions"])]
    _orphanedCollections = []
