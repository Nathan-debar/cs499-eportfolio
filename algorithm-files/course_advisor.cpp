//============================================================================
// Name        : Project2.cpp
// Author      : Nathan deBar
// Date        : April 15, 2025
//============================================================================

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
using namespace std;

class Course {
public:
    string courseNumber;
    string title;
    vector<string> prerequisites;

    // Constructor
    Course(string number, string courseTitle)
        : courseNumber(number), title(courseTitle) {}

    // Method to add prerequisites
    void addPrerequisite(string prerequisite) {
        prerequisites.push_back(prerequisite);
    }

    // Method to display course details
    void printCourseInfo() const {
        cout << "Course: " << title << " (" << courseNumber << ")" << endl;
        cout << "Prerequisites: ";
        if (prerequisites.empty()) {
            cout << "None";
        } else {
            for (const auto& prereq : prerequisites) {
                cout << prereq << " ";
            }
        }
        cout << endl;
    }
};

void loadCoursesFromFile(const string& filename, vector<Course>& courses) {
    ifstream file(filename);
    if (!file) {
        cerr << "Error opening file." << endl;
        return;
    }

    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string courseNumber, title, prerequisite;
        
        // Read the course number and title
        getline(ss, courseNumber, ',');
        getline(ss, title, ',');

        Course newCourse(courseNumber, title);

        // Read prerequisites (if any)
        while (getline(ss, prerequisite, ',')) {
            if (!prerequisite.empty()) {
                newCourse.addPrerequisite(prerequisite);
            }
        }

        // Add course to the list
        courses.push_back(newCourse);
    }

    file.close();
}

void printSortedCourses(const vector<Course>& courses) {
    vector<Course> sortedCourses = courses;
    sort(sortedCourses.begin(), sortedCourses.end(), [](const Course& a, const Course& b) {
        return a.courseNumber < b.courseNumber;
    });

    for (const auto& course : sortedCourses) {
        cout << course.courseNumber << ": " << course.title << endl;
    }
}

void printCourseInfoByNumber(const vector<Course>& courses, const string& courseNumber) {
    for (const auto& course : courses) {
        if (course.courseNumber == courseNumber) {
            course.printCourseInfo();
            return;
        }
    }
    cout << "Course not found." << endl;
}

void showMenu() {
    cout << "1. Load course data from file" << endl;
    cout << "2. Print alphanumeric list of all courses" << endl;
    cout << "3. Print course title and prerequisites by course number" << endl;
    cout << "9. Exit" << endl;
}

int main() {
    vector<Course> courses;
    int choice;
    string filename = "CS 300 ABCU_Advising_Program_Input.csv"; // File name 

    while (true) {
        showMenu();
        cout << "Enter your choice: ";
        cin >> choice;
        cin.ignore(); // to ignore any newline character left in the input buffer

        switch (choice) {
            case 1:
                loadCoursesFromFile(filename, courses);
                cout << "Data loaded successfully." << endl;
                break;

            case 2:
                printSortedCourses(courses);
                break;

            case 3:
                {
                    string courseNumber;
                    cout << "Enter course number: ";
                    cin >> courseNumber;
                    printCourseInfoByNumber(courses, courseNumber);
                }
                break;

            case 9:
                cout << "Exiting program." << endl;
                return 0;

            default:
                cout << "Invalid choice. Please try again." << endl;
        }
    }
}
