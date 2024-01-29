class DatabaseClient:
    def name_to_nn(self, name):
        """
        Given a member's name, fuzzy match to search for an Active install
        and return that install's NN, or None if not found
        """
        raise NotImplementedError()

    def email_to_nn(self, email):
        """
        Given a member's email, search for an Active install
        and return that install's NN, or None if not found
        """
        raise NotImplementedError()

    def nn_to_linked_nn(self, nn):
        """
        Given an NN, return a list of the NNs of all directly adjacent nodes
        using the Links table or None if the NN is not found
        """
        raise NotImplementedError()

    def get_nn(self, input_number):
        """
        Given an input number which might be an NN or install number,
        search for an Active install and return that install's NN,
        or None if not found
        """
        raise NotImplementedError()

    def nn_to_location(self, nn):
        """
        Given an NN, return the lat/lon of the underlying building as a dict:
        {"Latitude": ..., "Longitude": ...}
        or None if the NN is not found
        """
        raise NotImplementedError()
