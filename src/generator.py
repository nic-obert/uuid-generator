import random
import json


class UUIDNode:

    __slots__ = ("uuid", "lesser", "greater")

    def __init__(self, uuid: int) -> None:
        self.uuid = uuid
        self.lesser: UUIDNode | None = None
        self.greater: UUIDNode | None = None

    
    def to_dict(self) -> dict:
        d = {}

        if self.lesser is not None:
            d["lesser"] = self.lesser.to_dict()
        if self.greater is not None:
            d["greater"] = self.greater.to_dict()

        return {
            self.uuid: d
        }


class UUIDTree:

    __slots__ = ("root")

    def __init__(self) -> None:
        self.root: UUIDNode | None = None
    

    def find(self, uuid: int) -> bool:
        if not self.root:
            return False

        node = self.root
        while node:

            if node.uuid == uuid:
                return True
            
            if node.uuid > uuid:
                node = node.lesser
            else:
                node = node.greater
            
        return False


    def _insert_from_node(self, node: UUIDNode, uuid: int) -> bool:
        while node:

            # Check if the node already exists
            if node.uuid == uuid:
                return False
            
            if node.uuid > uuid:
                if node.lesser:
                    node = node.lesser
                else:
                    # Append the new node to the end of the tree
                    node.lesser = UUIDNode(uuid)
                    return True

            else: # if node.uuid < uuid
                if node.greater:
                    node = node.greater
                else:
                    # Append the new node to the end of the tree
                    node.greater = UUIDNode(uuid)
                    return True

        return False
    

    def _send_down_node_from_node(self, from_node: UUIDNode, node: UUIDNode) -> None:
        while True:

            # Assume there are no duplicates in the tree
            if from_node.uuid > node.uuid:
                if from_node.lesser:
                    from_node = node.lesser
                else:
                    # Append the new node to the end of the tree
                    node.lesser = from_node
                    return
            
            else: # if from_node.uuid < node.uuid
                if from_node.greater:
                    from_node = node.greater
                else:
                    # Append the new node to the end of the tree
                    node.greater = from_node
                    return


    def insert(self, uuid: int) -> bool:
        """
            Inserts a new node into the tree.
            Returns True if the node was inserted, False if it was already in the tree.
        """
        if not self.root:
            self.root = UUIDNode(uuid)
            return True
        
        return self._insert_from_node(self.root, uuid)
    

    def delete(self, uuid: int) -> bool:
        """
            Deletes a node from the tree.
            Returns True if the node was deleted, False if it was not in the tree.
        """
        if not self.root:
            return False

        parent: UUIDNode | None = None
        node = self.root
        while node:

            # The node to delete has been found
            if node.uuid == uuid:
                if node.lesser and node.greater:
                    # The current node has two children
                    # Choose the smallest child of the current node to replace the current node
                    # because it will always be bigger than the parent node
                    if parent:
                        # The current node is not the root node
                        if parent.lesser == node:
                            parent.lesser = node.lesser
                        else:
                            parent.greater = node.lesser
                                            
                    else:
                        # The current node is the root node
                        self.root = node.lesser

                    # Send the other node down the tree
                    self._send_down_node_from_node(node.lesser, node.greater)
                    return True

                if node.lesser:
                    if parent:
                        # The current node is not the root node
                        if parent.lesser == node:
                            parent.lesser = node.lesser
                        else:
                            parent.greater = node.lesser
                    else:
                        # The current node is the root node
                        self.root = node.lesser
                    
                    return True

                if node.greater:
                    if parent:
                        # The current node is not the root node
                        if parent.lesser == node:
                            parent.lesser = node.greater
                        else:
                            parent.greater = node.greater
                    else:
                        # The current node is the root node
                        self.root = node.greater

                    return True
                
                # The current node has no children
                if parent:
                    # The current node is not the root node
                    if parent.lesser == node:
                        parent.lesser = None
                    else:
                        parent.greater = None
                else:
                    # The current node is the root node
                    self.root = None

                return True

            if node.uuid > uuid:
                node = node.lesser
            else: # if node.uuid < uuid
                node = node.greater

        return False

    
    def toJSON(self) -> str:
        dict_repr = {}
        
        if self.root:
            dict_repr["root"] = self.root.to_dict()
        
        return json.dumps(dict_repr, indent=2)


class UUIDGenerator:

    __slots__ = ("_seed", "uuids")

    def __init__(self, seed: int | None = None) -> None:
        if seed:
            self.seed(seed)
        self.uuids = UUIDTree()


    def seed(self, seed: int) -> None:
        """
            Sets the seed for the random number generator.
        """
        self._seed = seed
        random.seed(seed)


    def generate(self) -> int:
        """
            Generates a new UUID.
            Returns the UUID.
        """
        while True:
            uuid = random.randint(0, 2**128 - 1)
            if self.uuids.insert(uuid):
                return uuid       


    def exists(self, uuid: int) -> bool:
        """
            Checks if a UUID exists in the tree.
            Returns True if the UUID exists, False if it does not.
        """
        return self.uuids.find(uuid)

    
    def delete(self, uuid: int) -> bool:
        """
            Deletes a UUID from the tree.
            Returns True if the UUID was deleted, False if it was not in the tree.
        """
        return self.uuids.delete(uuid)


    def __str__(self) -> str:
        return self.uuids.toJSON()

    
    def __repr__(self) -> str:
        return str(self)


class UUIDGeneratorDict:

    __slots__ = ("_seed", "uuids")

    def __init__(self, seed: int | None = None) -> None:
        if seed:
            self.seed(seed)
        self.uuids = {}


    def seed(self, seed: int) -> None:
        """
            Sets the seed for the random number generator.
        """
        self._seed = seed
        random.seed(seed)


    def generate(self) -> int:
        """
            Generates a new UUID.
            Returns the UUID.
        """
        while True:
            uuid = random.randint(0, 2**128 - 1)
            if uuid not in self.uuids:
                self.uuids[uuid] = True
                return uuid


    def exists(self, uuid: int) -> bool:
        """
            Checks if a UUID exists in the tree.
            Returns True if the UUID exists, False if it does not.
        """
        return uuid in self.uuids

    
    def delete(self, uuid: int) -> bool:
        """
            Deletes a UUID from the tree.
            Returns True if the UUID was deleted, False if it was not in the tree.
        """
        if uuid in self.uuids:
            del self.uuids[uuid]
            return True
        return False


    def __str__(self) -> str:
        return json.dumps(self.uuids, indent=2)

    
    def __repr__(self) -> str:
        return str(self)