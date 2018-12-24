# iSpace_Downloader
Easy way to download "all" course resources at iSpace (Moodle driven)

# Requirement
- Python 3+
- Beautiful Soup 4.4.0+

## How to use
### Way 1
1. Directly run
2. Input `username` and `password`
  - Then the courses will loaded and display with a index number
3. Type-in the index number to select the course
  - All course resources will load and a summary will display
  - Ask whether the user want to download or not
4. Type your download intention ([Y/n])
  - If you don't program, it will terminate itself
5. Download started, files will be download to `./download/[course_name]`

### Way 2
1. Use your text editor to modify `username` and `password` fields in the 9 and 10 line of the `main.py` file
2. Directly run
  - Then the courses will loaded and display with a index number
3. Type-in the index number to select the course
  - All course resources will load and a summary will display
  - Ask whether the user want to download or not
4. Type your download intention ([Y/n])
  - If you don't program, it will terminate itself
5. Download started, files will be download to `./download/[course_name]`
