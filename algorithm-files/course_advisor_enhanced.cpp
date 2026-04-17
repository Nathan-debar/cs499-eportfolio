#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <unordered_map>
using namespace std;

class Course {
public:
    string courseNumber;
    string title;
    vector<string> prerequisites;

    Course() = default;

    // Constructor initializes course data
    Course(string number, string courseTitle)
        : courseNumber(number), title(courseTitle) {}

    // Add prerequisite to the list
    void addPrerequisite(const string& prerequisite) {
        prerequisites.push_back(prerequisite);
    }

    // Display course details and prerequisites
    void printCourseInfo() const {
        cout << "Course: " << courseNumber << ", " << title << endl;
        cout << "Prerequisites: ";

        if (prerequisites.empty()) {
            cout << "None";
        } else {
            // Print all prerequisites separated by commas
            for (size_t i = 0; i < prerequisites.size(); ++i) {
                cout << prerequisites[i];
                if (i < prerequisites.size() - 1) {
                    cout << ", ";
                }
            }
        }
        cout << endl;
    }
};

// Load course data from file into hash table
void loadCoursesFromFile(const string& filename, unordered_map<string, Course>& courses) {
    ifstream file(filename);

    if (!file) {
        cerr << "Error opening file." << endl;
        return;
    }

    courses.clear(); // Ensure no duplicate loading

    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string courseNumber, title, prerequisite;

        // Extract course number and title
        getline(ss, courseNumber, ',');
        getline(ss, title, ',');

        // Skip invalid rows
        if (courseNumber.empty() || title.empty()) {
            continue;
        }

        Course newCourse(courseNumber, title);

        // Extract any prerequisites
        while (getline(ss, prerequisite, ',')) {
            if (!prerequisite.empty()) {
                newCourse.addPrerequisite(prerequisite);
            }
        }

        // Store course using courseNumber as key for fast lookup
        courses[courseNumber] = newCourse;
    }

    file.close();
}

// Print all courses in sorted order (by course number)
void printSortedCourses(const unordered_map<string, Course>& courses) {
    vector<string> courseNumbers;

    // Extract keys from hash table
    for (const auto& pair : courses) {
        courseNumbers.push_back(pair.first);
    }

    // Sort keys alphabetically
    sort(courseNumbers.begin(), courseNumbers.end());

    // Print sorted results
    for (const auto& number : courseNumbers) {
        cout << number << ": " << courses.at(number).title << endl;
    }
}

// Retrieve and print course info using fast hash lookup
void printCourseInfoByNumber(const unordered_map<string, Course>& courses, const string& courseNumber) {
    auto it = courses.find(courseNumber); // O(1) average lookup

    if (it != courses.end()) {
        it->second.printCourseInfo();
    } else {
        cout << "Course not found." << endl;
    }
}

void showMenu() {
    cout << endl;
    cout << "1. Load course data from file" << endl;
    cout << "2. Print alphanumeric list of all courses" << endl;
    cout << "3. Print course title and prerequisites by course number" << endl;
    cout << "9. Exit" << endl;
}

int main() {
    unordered_map<string, Course> courses; // Replaces vector for faster access
    int choice = 0;
    string filename = "CS 300 ABCU_Advising_Program_Input.csv";

    while (true) {
        showMenu();
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
        case 1:
            loadCoursesFromFile(filename, courses);
            cout << "Data loaded successfully." << endl;
            break;

        case 2:
            // Prevent running before data is loaded
            if (courses.empty()) {
                cout << "No course data loaded." << endl;
                break;
            }
            printSortedCourses(courses);
            break;

        case 3: {
            if (courses.empty()) {
                cout << "No course data loaded." << endl;
                break;
            }

            string courseNumber;
            cout << "Enter course number: ";
            cin >> courseNumber;

            // Normalize input (ensures match with stored keys)
            transform(courseNumber.begin(), courseNumber.end(), courseNumber.begin(), ::toupper);

            printCourseInfoByNumber(courses, courseNumber);
            break;
        }

        case 9:
            cout << "Exiting program." << endl;
            return 0;

        default:
            cout << "Invalid choice. Please try again." << endl;
        }
    }
}