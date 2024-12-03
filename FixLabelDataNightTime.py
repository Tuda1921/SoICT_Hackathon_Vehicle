import os

label_data = r'D:\Tuda\SoICT_Hackathon_Vehicle\datasets-full\coco8\labels\train'

# Iterate over the files in the label directory
for filename in os.listdir(label_data):
    file_path = os.path.join(label_data, filename)

    if os.path.isfile(file_path) and filename.endswith('.txt'):
        try:
            # Read the content of the file
            with open(file_path, 'r') as file:
                content = file.readlines()

            modified_content = []
            for line in content:
                line = line.split()
                if line:  # Ensure the line is not empty
                    line[0] = str(int(float(line[0])))  # Convert the first value to an integer
                    modified_content.append(' '.join(line))

            # Write the modified content back to the file
            with open(file_path, 'w') as file:
                for line in modified_content:
                    file.write(line + '\n')
        except Exception as e:
            print(f"Error processing {filename}: {e}")
