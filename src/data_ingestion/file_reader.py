import json
import os


class FileReader:

    @classmethod
    def read_txt_file(cls, filename):
        """
        Reads the content of a .txt file from the input/ folder and returns it as a string.

        Args:
            filename (str): The name of the .txt file (e.g., 'example.txt').

        Returns:
            str: The content of the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If there's an error reading the file.
        """
        file_path = os.path.join("input", filename)
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    @classmethod
    def read_json_file(cls, filename):
        """
        Reads the content of a .json file from the input/ folder and returns it as a dict.

        Args:
            filename (str): The name of the .json file (e.g., 'example.json').

        Returns:
            dict: The parsed JSON content.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If there's an error reading the file.
            json.JSONDecodeError: If the file is not valid JSON.
        """
        file_path = os.path.join("input", filename)
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
