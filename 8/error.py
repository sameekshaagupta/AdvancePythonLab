class FileNotFoundError(Exception):
    """Custom exception for file not found."""
    def __init__(self, filepath):
        super().__init__(f"File not found: {filepath}")


class InvalidInputDataError(Exception):
    """Custom exception for invalid input data."""
    def __init__(self, message):
        super().__init__(f"Invalid input data: {message}")


class DiskSpaceFullError(Exception):
    """Custom exception for disk space full."""
    def __init__(self, filepath):
        super().__init__(f"Insufficient disk space to write to: {filepath}")


def read_input_file(filepath):
    try:
        with open(filepath, 'r') as file:
            data = file.read()
            if not isinstance(data, str) or data.strip() == "":
                raise InvalidInputDataError("The file contains non-string or missing data.")
            return data
    except FileNotFoundError as e:
        raise FileNotFoundError(filepath) from e


def process_text(data):
    try:
        words = data.split()
        word_count = len(words)
        char_freq = {}
        for char in data:
            if char.isalpha():
                char_freq[char] = char_freq.get(char, 0) + 1
        return word_count, char_freq
    except Exception as e:
        raise InvalidInputDataError("An error occurred during text processing.") from e


def write_output_file(filepath, word_count, char_freq):
    try:
        with open(filepath, 'w') as file:
            file.write(f"Word Count: {word_count}\n")
            file.write("Character Frequencies:\n")
            for char, freq in char_freq.items():
                file.write(f"{char}: {freq}\n")
    except IOError as e:
        if "No space left on device" in str(e):
            raise DiskSpaceFullError(filepath) from e
        else:
            raise


def main(input_filepath, output_filepath):
    try:
        # Step 1: Read input file
        text_data = read_input_file(input_filepath)

        # Step 2: Process text data
        word_count, char_freq = process_text(text_data)

        # Step 3: Write output file
        write_output_file(output_filepath, word_count, char_freq)

        print("Text processing completed successfully.")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except InvalidInputDataError as iide_error:
        print(iide_error)
    except DiskSpaceFullError as dsf_error:
        print(dsf_error)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Example usage:
input_filepath = "input.txt"  # Replace with the actual input file path
output_filepath = "output.txt"  # Replace with the actual output file path
main(input_filepath, output_filepath)
