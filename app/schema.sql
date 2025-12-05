-- Reset Tables

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS MatchParticipation;
DROP TABLE IF EXISTS StudentInterest;
DROP TABLE IF EXISTS StudentSkill;
DROP TABLE IF EXISTS Organizes;
DROP TABLE IF EXISTS Attends;
DROP TABLE IF EXISTS Enrollment;
DROP TABLE IF EXISTS `Match`;
DROP TABLE IF EXISTS AvailabilitySlot;
DROP TABLE IF EXISTS Interest;
DROP TABLE IF EXISTS Skill;
DROP TABLE IF EXISTS Experience;
DROP TABLE IF EXISTS `Event`;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Student;

SET FOREIGN_KEY_CHECKS = 1;

-- Table Creation

CREATE TABLE Student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name  VARCHAR(50) NOT NULL,
    email      VARCHAR(100) UNIQUE NOT NULL,
    grad_year  INT,
    password   VARCHAR(255) NOT NULL,
    profile_pic VARCHAR(255) DEFAULT NULL,
    CONSTRAINT check_grad_year CHECK (grad_year BETWEEN 2025 AND 2035)
);

CREATE TABLE Course (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    title     VARCHAR(100) NOT NULL,
    year      INT NOT NULL,
    section   VARCHAR(10)
);

CREATE TABLE `Event` (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(50),
    start_datetime DATETIME NOT NULL,
    end_datetime   DATETIME NOT NULL,
    location VARCHAR(100)
);

CREATE TABLE Experience (
    experience_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    job_title VARCHAR(100),
    organization VARCHAR(100),
    start_date DATE,
    end_date DATE,
    description TEXT,
    CONSTRAINT fk_experience_student
      FOREIGN KEY (student_id) REFERENCES Student(student_id)
      ON DELETE CASCADE
);

CREATE TABLE Skill (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Interest (
    interest_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE AvailabilitySlot (
    slot_id     INT AUTO_INCREMENT PRIMARY KEY,
    student_id  INT NOT NULL,
    start_time  TIME NOT NULL,
    end_time    TIME NOT NULL,
    day_of_week VARCHAR(10),
    CONSTRAINT fk_avail_student
      FOREIGN KEY (student_id) REFERENCES Student(student_id)
      ON DELETE CASCADE,
    INDEX idx_avail_student (student_id)
);

CREATE TABLE `Match` (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(50),
    match_score DECIMAL(5,2),
    capacity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Enrollment (
    student_id INT NOT NULL,
    course_id  INT NOT NULL,
    PRIMARY KEY (student_id, course_id),
    CONSTRAINT fk_enroll_student
      FOREIGN KEY (student_id) REFERENCES Student(student_id)
      ON DELETE CASCADE,
    CONSTRAINT fk_enroll_course
      FOREIGN KEY (course_id)  REFERENCES Course(course_id)
      ON DELETE CASCADE
);

CREATE TABLE Attends (
    student_id INT NOT NULL,
    event_id   INT NOT NULL,
    PRIMARY KEY (student_id, event_id),
    CONSTRAINT fk_attends_student
      FOREIGN KEY (student_id) REFERENCES Student(student_id)
      ON DELETE CASCADE,
    CONSTRAINT fk_attends_event
      FOREIGN KEY (event_id) REFERENCES `Event`(event_id)
      ON DELETE CASCADE
);

CREATE TABLE Organizes (
    student_id INT NOT NULL,
    event_id   INT NOT NULL,
    PRIMARY KEY (student_id, event_id),
    CONSTRAINT fk_org_student
      FOREIGN KEY (student_id) REFERENCES Student(student_id)
      ON DELETE CASCADE,
    CONSTRAINT fk_org_event
      FOREIGN KEY (event_id) REFERENCES `Event`(event_id)
      ON DELETE CASCADE
);

CREATE TABLE StudentSkill (
    student_id INT NOT NULL,
    skill_id   INT NOT NULL,
    PRIMARY KEY (student_id, skill_id),
    CONSTRAINT fk_ss_student
      FOREIGN KEY (student_id) REFERENCES Student(student_id)
      ON DELETE CASCADE,
    CONSTRAINT fk_ss_skill
      FOREIGN KEY (skill_id) REFERENCES Skill(skill_id)
      ON DELETE CASCADE
);

CREATE TABLE StudentInterest (
    student_id  INT NOT NULL,
    interest_id INT NOT NULL,
    PRIMARY KEY (student_id, interest_id),
    CONSTRAINT fk_si_student
      FOREIGN KEY (student_id) REFERENCES Student(student_id)
      ON DELETE CASCADE,
    CONSTRAINT fk_si_interest
      FOREIGN KEY (interest_id) REFERENCES Interest(interest_id)
      ON DELETE CASCADE
);

CREATE TABLE MatchParticipation (
    student_id INT NOT NULL,
    match_id   INT NOT NULL,
    PRIMARY KEY (student_id, match_id),
    CONSTRAINT fk_mp_student
      FOREIGN KEY (student_id) REFERENCES Student(student_id)
      ON DELETE CASCADE,
    CONSTRAINT fk_mp_match
      FOREIGN KEY (match_id) REFERENCES `Match`(match_id)
      ON DELETE CASCADE
);

-- Stored Procedure

DROP PROCEDURE IF EXISTS update_grad_year;

DELIMITER $$
CREATE PROCEDURE update_grad_year (
    IN p_student_id INT,
    IN p_new_grad_year INT
)
BEGIN
    UPDATE Student
    SET grad_year = p_new_grad_year
    WHERE student_id = p_student_id;
END$$
DELIMITER ;

-- Insert Students
INSERT INTO Student (first_name, last_name, email, grad_year, password) VALUES
('Maddie', 'Wise', 'mw5q@virginia.edu', 2025, 'password123'),
('Connor', 'Brooks', 'cb2x@virginia.edu', 2026, 'password123'),
('Eva', 'Butler', 'eb3x@virginia.edu', 2025, 'password123'),
('Nishana', 'Dahal', 'nd4k@virginia.edu', 2027, 'password123'),
('Ava', 'Li', 'al8g@virginia.edu', 2025, 'password123'),
('James', 'Patel', 'jp9r@virginia.edu', 2026, 'password123'),
('Sofia', 'Nguyen', 'sn2p@virginia.edu', 2025, 'password123'),
('Noah', 'Kim', 'nk3v@virginia.edu', 2025, 'password123'),
('Isabella', 'Smith', 'is6b@virginia.edu', 2025, 'password123'),
('Ethan', 'Johnson', 'ej5f@virginia.edu', 2026, 'password123'),
('Oliver', 'Garcia', 'og2t@virginia.edu', 2025, 'password123'),
('Charlotte', 'Davis', 'cd4u@virginia.edu', 2025, 'password123'),
('Amelia', 'Clark', 'ac7y@virginia.edu', 2026, 'password123'),
('Liam', 'Perez', 'lp8a@virginia.edu', 2027, 'password123'),
('Mia', 'Bennett', 'mb1m@virginia.edu', 2025, 'password123'),
('William', 'Roberts', 'wr9n@virginia.edu', 2025, 'password123'),
('Benjamin', 'Mitchell', 'bm2l@virginia.edu', 2026, 'password123'),
('Ella', 'Lopez', 'el5z@virginia.edu', 2025, 'password123'),
('Lucas', 'Rivera', 'lr3x@virginia.edu', 2025, 'password123'),
('Harper', 'Gonzalez', 'hg6v@virginia.edu', 2026, 'password123'),
('Michael', 'Lee', 'ml9c@virginia.edu', 2027, 'password123'),
('Grace', 'Adams', 'ga4s@virginia.edu', 2025, 'password123'),
('Henry', 'Torres', 'ht7w@virginia.edu', 2025, 'password123'),
('Aiden', 'Morris', 'am1r@virginia.edu', 2026, 'password123'),
('Chloe', 'Morgan', 'cm3e@virginia.edu', 2025, 'password123'),
('Ella', 'Nelson', 'en9p@virginia.edu', 2026, 'password123'),
('Sebastian', 'Ward', 'sw4u@virginia.edu', 2025, 'password123'),
('Abigail', 'Baker', 'ab6o@virginia.edu', 2025, 'password123'),
('Jack', 'Hall', 'jh2t@virginia.edu', 2027, 'password123'),
('Samantha', 'Graham', 'sg8c@virginia.edu', 2025, 'password123'),
('Ana', 'Doe', 'dde3@virginia.edu', 2026, 'securePass123');

-- Set variable for the last inserted student (Ana Doe)
SET @student_id = LAST_INSERT_ID();

-- Insert Courses
INSERT INTO Course (title, year, section) VALUES
('CS 4750 - Database Systems', 2025, '001'),
('CS 3240 - Advanced Software Development', 2025, '001'),
('STS 1500 - Engineers in Society', 2025, '002'),
('COMM 2010 - Accounting', 2025, '001'),
('ECON 2010 - Microeconomics', 2025, '001'),
('APMA 1110 - Calculus II', 2025, '001'),
('CS 2150 - Program and Data Representation', 2025, '001'),
('CS 4102 - Algorithms', 2025, '001'),
('ENGR 1620 - Introduction to Engineering', 2025, '001'),
('COMM 3010 - Marketing', 2025, '001'),
('MATH 3350 - Applied Linear Algebra', 2025, '001'),
('CS 4640 - Web Development', 2025, '001'),
('CS 3330 - Computer Architecture', 2025, '001'),
('PHYS 1425 - Intro Physics I', 2025, '001'),
('CS 4980 - Capstone Project', 2025, '001'),
('Database Systems', 2025, 'A');

SET @course_id = LAST_INSERT_ID();

-- Insert Events
INSERT INTO `Event` (title, description, type, start_datetime, end_datetime, location) VALUES
('HackUVA', 'Annual 24-hour hackathon for UVA students.', 'Tech', '2025-03-01 09:00:00', '2025-03-02 15:00:00', 'Rice Hall'),
('Startup Mixer', 'Networking event for founders and investors.', 'Career', '2025-03-10 18:00:00', '2025-03-10 20:00:00', 'Contemplative Commons'),
('Women in Tech Night', 'Celebration of women in computing at UVA.', 'Social', '2025-02-05 17:00:00', '2025-02-05 19:00:00', 'Newcomb Hall'),
('AI Research Symposium', 'Talks and poster sessions by UVA faculty.', 'Academic', '2025-04-15 10:00:00', '2025-04-15 17:00:00', 'Thornton Hall'),
('Hoos for Data', 'Workshop for data enthusiasts.', 'Workshop', '2025-02-20 14:00:00', '2025-02-20 16:00:00', 'Clark Library'),
('Cville Innovators', 'Charlottesville startup showcase.', 'Career', '2025-03-25 17:30:00', '2025-03-25 19:30:00', 'Darden School'),
('Hack4Humanity', 'Coding for social good.', 'Tech', '2025-04-10 09:00:00', '2025-04-11 15:00:00', 'Rice Hall'),
('CIO Fair', 'Showcase of UVA CIOs and student clubs.', 'Social', '2025-02-12 11:00:00', '2025-02-12 14:00:00', 'Amphitheater'),
('LinkedIn Headshots', 'Professional headshot session for students.', 'Career', '2025-02-28 13:00:00', '2025-02-28 16:00:00', 'Newcomb Ballroom'),
('Capstone Demo Day', 'Students present final projects.', 'Academic', '2025-05-02 09:00:00', '2025-05-02 12:00:00', 'Olsson Hall'),
('Career Fair', 'Meet employers on campus', 'Networking', '2025-04-10 10:00:00', '2025-04-10 14:00:00', 'Thornton Hall');

SET @event_id = LAST_INSERT_ID();

-- Insert Skill and Interest
INSERT INTO Skill (name) VALUES ('Python');
SET @skill_id = LAST_INSERT_ID();

INSERT INTO Interest (name) VALUES ('Artificial Intelligence');
SET @interest_id = LAST_INSERT_ID();

-- Insert Match
INSERT INTO `Match` (status, match_score, capacity) VALUES ('Pending', 87.5, 3);
SET @match_id = LAST_INSERT_ID();

-- Insert dependent rows using the IDs
INSERT INTO Experience (student_id, job_title, organization, start_date, end_date, description) VALUES
(@student_id, 'Intern', 'Microsoft', '2024-06-01', '2024-08-30', 'Worked on backend development for Azure cloud services.');

INSERT INTO AvailabilitySlot (student_id, start_time, end_time, day_of_week) VALUES
(@student_id, '09:00:00', '10:00:00', 'Monday');

INSERT INTO Enrollment (student_id, course_id) VALUES
(@student_id, @course_id);

INSERT INTO Attends (student_id, event_id) VALUES
(@student_id, @event_id);

INSERT INTO Organizes (student_id, event_id) VALUES
(@student_id, @event_id);

INSERT INTO StudentSkill (student_id, skill_id) VALUES
(@student_id, @skill_id);

INSERT INTO StudentInterest (student_id, interest_id) VALUES
(@student_id, @interest_id);

INSERT INTO MatchParticipation (student_id, match_id) VALUES
(@student_id, @match_id);

-- Retrieve statements
-- Retrieve all students
SELECT * FROM Student;

-- Retrieve student names and emails graduating in 2025
SELECT first_name, last_name, email
FROM Student
WHERE grad_year = 2025;

-- Retrieve students ordered by graduation year (soonest first)
SELECT first_name, last_name, grad_year
FROM Student
ORDER BY grad_year ASC;

-- Retrieve all courses
SELECT * FROM Course;

-- Retrieve all CS courses
SELECT * 
FROM Course
WHERE title LIKE 'CS%';

-- Count how many courses are offered by department prefix
SELECT SUBSTRING_INDEX(title, ' ', 1) AS department, COUNT(*) AS num_courses
FROM Course
GROUP BY department;

-- Retrieve all upcoming events
SELECT title, type, start_datetime, location
FROM `Event`
WHERE start_datetime > NOW()
ORDER BY start_datetime ASC;

-- Retrieve events by type
SELECT type, COUNT(*) AS total_events
FROM `Event`
GROUP BY type;

-- Retrieve events happening in March
SELECT title, start_datetime
FROM `Event`
WHERE MONTH(start_datetime) = 3;

-- Retrieve all experiences per student
SELECT s.first_name, s.last_name, e.job_title, e.organization
FROM Experience e
JOIN Student s ON e.student_id = s.student_id;

-- Retrieve most common organizations students worked at
SELECT organization, COUNT(*) AS total
FROM Experience
GROUP BY organization
ORDER BY total DESC;

-- Retrieve all skills
SELECT * FROM Skill;

-- Retrieve students with a specific skill (Python)
SELECT s.first_name, s.last_name
FROM StudentSkill ss
JOIN Student s ON ss.student_id = s.student_id
JOIN Skill sk ON ss.skill_id = sk.skill_id
WHERE sk.name = 'Python';

-- Retrieve all interests
SELECT * FROM Interest;

-- Retrieve students interested in 'Artificial Intelligence'
SELECT s.first_name, s.last_name
FROM StudentInterest si
JOIN Student s ON si.student_id = s.student_id
JOIN Interest i ON si.interest_id = i.interest_id
WHERE i.name = 'Artificial Intelligence';

-- Retrieve all availability slots
SELECT * FROM AvailabilitySlot;

-- Retrieve students available on Fridays
SELECT s.first_name, s.last_name, a.start_time, a.end_time
FROM AvailabilitySlot a
JOIN Student s ON a.student_id = s.student_id
WHERE a.day_of_week = 'Friday';

-- Retrieve all matches
SELECT * FROM `Match`;

-- Retrieve top matches by score
SELECT match_id, status, match_score
FROM `Match`
ORDER BY match_score DESC
LIMIT 10;

-- Retrieve all enrollments
SELECT * FROM Enrollment;

-- Retrieve courses each student is enrolled in
SELECT s.first_name, s.last_name, c.title
FROM Enrollment e
JOIN Student s ON e.student_id = s.student_id
JOIN Course c ON e.course_id = c.course_id
ORDER BY s.last_name;

-- Retrieve total students per course
SELECT c.title, COUNT(e.student_id) AS num_students
FROM Enrollment e
JOIN Course c ON e.course_id = c.course_id
GROUP BY c.title
ORDER BY num_students DESC;

-- Retrieve all event attendance
SELECT s.first_name, s.last_name, e.title AS event_title
FROM Attends a
JOIN Student s ON a.student_id = s.student_id
JOIN `Event` e ON a.event_id = e.event_id;

-- Retrieve attendance count per event
SELECT e.title, COUNT(a.student_id) AS attendees
FROM Attends a
JOIN `Event` e ON a.event_id = e.event_id
GROUP BY e.title
ORDER BY attendees DESC;

-- Retrieve all organizers and their events
SELECT s.first_name, s.last_name, e.title
FROM Organizes o
JOIN Student s ON o.student_id = s.student_id
JOIN `Event` e ON o.event_id = e.event_id;

-- Retrieve number of events each student organized
SELECT s.first_name, s.last_name, COUNT(o.event_id) AS events_organized
FROM Organizes o
JOIN Student s ON o.student_id = s.student_id
GROUP BY s.student_id
ORDER BY events_organized DESC;

-- Retrieve all student-skill relationships
SELECT s.first_name, s.last_name, sk.name AS skill
FROM StudentSkill ss
JOIN Student s ON ss.student_id = s.student_id
JOIN Skill sk ON ss.skill_id = sk.skill_id
ORDER BY s.last_name;

-- Retrieve all student-interest relationships
SELECT s.first_name, s.last_name, i.name AS interest
FROM StudentInterest si
JOIN Student s ON si.student_id = s.student_id
JOIN Interest i ON si.interest_id = i.interest_id
ORDER BY s.last_name;

-- Retrieve which students are in which match
SELECT s.first_name, s.last_name, m.match_id, m.status, m.match_score
FROM MatchParticipation mp
JOIN Student s ON mp.student_id = s.student_id
JOIN `Match` m ON mp.match_id = m.match_id
ORDER BY m.match_id;

-- Retrieve number of participants per match
SELECT m.match_id, COUNT(mp.student_id) AS participants
FROM MatchParticipation mp
JOIN `Match` m ON mp.match_id = m.match_id
GROUP BY m.match_id
ORDER BY participants DESC;

-- Update statements

UPDATE Student 
SET grad_year = 2027, password = 'newSecurePass!' 
WHERE student_id = 1;

UPDATE Course
SET title = 'Advanced Database Systems'
WHERE course_id = 1;

UPDATE `Event`
SET location = 'Thornton Hall - Room 201'
WHERE event_id = 1;

UPDATE Experience
SET job_title = 'Software Engineer Intern'
WHERE experience_id = 1;

UPDATE Skill
SET name = 'Advanced Python'
WHERE skill_id = 1;

UPDATE Interest
SET name = 'Machine Learning'
WHERE interest_id = 1;

UPDATE AvailabilitySlot
SET end_time = '10:30:00'
WHERE slot_id = 1;

UPDATE `Match`
SET status = 'Confirmed', match_score = 90
WHERE match_id = 1;

UPDATE Enrollment
SET course_id = 2
WHERE student_id = 1 AND course_id = 1;

UPDATE Attends
SET event_id = 2
WHERE student_id = 1 AND event_id = 1;

UPDATE Organizes
SET event_id = 2
WHERE student_id = 1 AND event_id = 1;

UPDATE StudentSkill
SET skill_id = 1
WHERE student_id = 1 AND skill_id = 1;

UPDATE StudentInterest
SET interest_id = 1
WHERE student_id = 1 AND interest_id = 1;

UPDATE MatchParticipation
SET match_id = 1
WHERE student_id = 1 AND match_id = 1;

-- Delete Commands

DELETE FROM Student
WHERE student_id = 1;

DELETE FROM Course
WHERE course_id = 1;

DELETE FROM `Event`
WHERE event_id = 1;

DELETE FROM Experience
WHERE experience_id = 1;

DELETE FROM Skill
WHERE skill_id = 1;

DELETE FROM Interest
WHERE interest_id = 1;

DELETE FROM AvailabilitySlot
WHERE slot_id = 1 AND student_id = 1;

DELETE FROM `Match`
WHERE match_id = 1;

DELETE FROM Enrollment
WHERE student_id = 1 AND course_id = 1;

DELETE FROM Attends
WHERE student_id = 1 AND event_id = 1;

DELETE FROM Organizes
WHERE student_id = 1 AND event_id = 1;

DELETE FROM StudentSkill
WHERE student_id = 1 AND skill_id = 1;

DELETE FROM StudentInterest
WHERE student_id = 1 AND interest_id = 1;

DELETE FROM MatchParticipation
WHERE student_id = 1 AND match_id = 1;
