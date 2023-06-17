import os
import pytest
from nnn import convert_csv_to_vcf
def test_convert_csv_to_vcf():
    # Use a sample csv file for the test
    test_file_path = "test.csv"
    output_file_path = "test.vcf"

    # Run the conversion function
    success_message = convert_csv_to_vcf(test_file_path, output_file_path)

    # Check if the vcf file is created
    assert os.path.exists(output_file_path)

    # Check the success message
    assert success_message == "File successfully converted."

def test_cleanup():
    # Cleanup the created vcf file after all tests
    if os.path.exists("test.vcf"):
        os.remove("test.vcf")

# Call cleanup function at the end of all tests
pytest.sessionfinish = test_cleanup

