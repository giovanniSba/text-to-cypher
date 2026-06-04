import os

from neo4j import GraphDatabase

_driver_instance = None

NEO4J_URI = os.environ.get("NEO4J_URI", "")
NEO4J_USER = os.environ.get("NEO4J_USER", "")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "")


def get_driver():
    """Singleton instance of neo4j driver."""
    global _driver_instance
    if _driver_instance is None:
        _driver_instance = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
        )
    return _driver_instance


def close_driver():
    """Close connection to neo4j."""
    global _driver_instance
    if _driver_instance is not None:
        _driver_instance.close()
        _driver_instance = None
