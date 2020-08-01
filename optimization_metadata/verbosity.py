# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


class VerbosityLVL0:
    def load_search_data(self, model):
        pass

    def load_search_data_success(self, model, dataframe):
        pass

    def save_search_data(self, model):
        pass

    def save_search_data_canceled(self, model):
        pass

    def save_search_data_success(self, model, dataframe):
        pass


class VerbosityLVL1:
    def load_search_data(self, model):
        print("Loading search data for", model.__name__, "...", end="\r")

    def load_search_data_success(self, model, dataframe):
        print(
            "Loading search data for",
            model.__name__,
            "was successful:",
            len(dataframe),
            "samples found",
        )

    def save_search_data(self, model):
        print("Saving search data for", model.__name__, "...", end="\r")

    def save_search_data_canceled(self, model):
        print(
            "Saving search data for",
            model.__name__,
            "was canceled. No new samples found",
        )

    def save_search_data_success(self, model, dataframe):
        print(
            "Saving search data for",
            model.__name__,
            "was successful:",
            len(dataframe),
            "new samples stored",
        )
