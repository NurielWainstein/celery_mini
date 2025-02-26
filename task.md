
# FastAPI Excel File Processor

This project demonstrates how to create a simple REST API using FastAPI that processes Excel files. The API is designed to organize and categorize Excel files based on specific attributes: **region**, **type**, and **category**.

### Concepts

1. **Region**:
   - Represents a geographical area.
   - Examples: "Asia", "Europe-West", etc.

2. **Type**:
   - A naming convention used to group files by category.
   - Examples: "sandwiches", "cars", "X", "Y", or any other agreed-upon term that describes the contents of the Excel file.

3. **Category**:
   - A label that combines **region** and **type** to define a group of Excel files.
   - Example: A category like "asian_phones" would include all Excel files that belong to the "phones" type and the "Asia" region.


# API Endpoints

## 1. `create_category(category_name, region, type)`
- **Description**: Creates a new category defined by a combination of **region** and **type**.
- **Parameters**:
  - `category_name`: The name you want to assign to the new category.
  - `region`: The geographical region associated with the category.
  - `type`: The type/category label that groups files (e.g., "sandwiches", "cars").
- **Function**: This will associate the specified region and type together under a new category name.

---

## 2. `upload_file(category_name, file)`
- **Description**: Uploads a file to a pre-existing category.
- **Parameters**:
  - `category_name`: The name of the category to which the file should be uploaded.
  - `file`: The file (presumably an Excel file) that will be uploaded and associated with that category.
- **Function**: This operation adds the provided file to the specified category, making it part of that region and type combination.

---

## 3. `sum_type(type)`
- **Description**: Calculates the sum of all numbers present in all Excel files in categories of the specified **type**.
- **Parameters**:
  - `type`: The type label for the category whose files should be summed up.
- **Function**: Returns the total sum of all numeric values found in the Excel files of categories under the given type. It aggregates data from all regions that have files of this type.

---

## 4. `find_regions(search_term)`
- **Description**: Finds regions where at least one Excel file contains the provided **search_term**.
- **Parameters**:
  - `search_term`: The term to search for within the contents of the Excel files in the categories.
- **Function**: Returns a list of all regions that have at least one Excel file containing the search term. This is useful to identify which geographical regions hold files with specific data of interest.

---


