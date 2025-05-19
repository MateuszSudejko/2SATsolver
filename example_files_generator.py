import random
import os


def generate_2sat_files(num_files, num_literals, num_clauses, output_dir="test_cases"):
    """
    Generate random 2SAT problem files.

    Args:
        num_files: Number of files to generate
        num_literals: Number of literals (variables) in each problem
        num_clauses: Number of clauses in each problem
        output_dir: Directory to save the generated files
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_idx in range(1, num_files + 1):
        # Generate random clauses
        clauses = []
        for _ in range(num_clauses):
            # Generate two random literals for each clause
            lit1 = random.randint(1, num_literals)
            lit2 = random.randint(1, num_literals)

            # Randomly negate literals
            if random.random() < 0.5:
                lit1 = -lit1
            if random.random() < 0.5:
                lit2 = -lit2

            # Ensure the two literals are different (optional)
            while lit1 == lit2 or lit1 == -lit2:
                lit2 = random.randint(1, num_literals)
                if random.random() < 0.5:
                    lit2 = -lit2

            clauses.append(f"{lit1} {lit2}")

        # Create the file content
        file_content = f"{num_literals}\n{';'.join(clauses)}"

        # Write to file
        file_path = os.path.join(output_dir, f"2sat_{file_idx}.txt")
        with open(file_path, 'w') as f:
            f.write(file_content)

        print(f"Generated file: {file_path}")


def main():
    print("2SAT Problem Generator")
    print("======================")

    try:
        num_files = int(input("Enter the number of files to generate: "))
        num_literals = int(input("Enter the number of literals (variables) per problem: "))
        num_clauses = int(input("Enter the number of clauses per problem: "))

        output_dir = input("Enter output directory (default: 'test_cases'): ")
        if not output_dir:
            output_dir = "test_cases"

        generate_2sat_files(num_files, num_literals, num_clauses, output_dir)
        print(f"\nSuccessfully generated {num_files} 2SAT problem files in '{output_dir}' directory.")

    except ValueError:
        print("Error: Please enter valid integer values.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
