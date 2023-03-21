import pymysql
import hashlib
from elements import User
import textwrap


def hash_pass(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def sql(func):
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except pymysql.err.OperationalError as error:
            raise DBEngine.DBException(error.args[1])
    return _wrapper


class DBEngine:
    def __init__(self):
        connection = pymysql.connect(host='localhost', user='root', password='1519582a', database='DLS')
        self.cursor = connection.cursor()
        self.user_id = None
        self.user_group = None

    @sql
    def add_user(self, mail, password, name):
        self.cursor.execute(f'insert Student(Mail, Pass, PersonName) values("{mail}", "{hash_pass(password)}", '
                            f'"{name}")')
        self.cursor.connection.commit()

    @sql
    def login(self, mail, password):
        self.cursor.execute(f'select PersonID, UserType from LoginTable where Mail = "{mail}" and '
                            f'Pass = "{hash_pass(password)}"')
        answer = self.cursor.fetchone()
        if answer is not None:
            self.user_id = answer[0]
            if answer[1] == User.STUDENT:
                self.user_group = "Student"
            else:
                self.user_group = "Worker"
            return answer[1]
        return None

    @sql
    def make_admin(self, role_id):
        self.cursor.execute(f'call MakePersonAdmin({self.user_id}, {role_id})')
        self.user_id = self.cursor.fetchone()[0]
        self.cursor.connection.commit()
        self.user_group = "Worker"

    @sql
    def get_person_info(self):
        information = ""
        headers = ["ФИО: ", "Почта: ", "Дата регистрации: "]
        if self.user_group == "Student":
            headers.append("Группа: ")
            self.cursor.execute(f'select PersonName, Mail, RegDate, GroupID from Student where '
                                f'PersonID = {self.user_id}')
            answer = self.cursor.fetchone()
            if answer[3] is not None:
                headers += ["Курс института: ", "Факультет: ", "Направление: "]
                self.cursor.execute(f'select GroupName, TrainingCourse, Faculty, Direction from StudentGroup where '
                                    f'GroupID = {answer[3]}')
                answer = answer[:-1] + self.cursor.fetchone()
        else:
            headers += ["Должность: ", "Обязанности: "]
            self.cursor.execute(f'select PersonName, Mail, RegDate, RoleID, WorkDescript from Worker where '
                                f'PersonID = {self.user_id}')
            answer = self.cursor.fetchone()
            if answer[3] is not None:
                headers.insert(4, "Деятельность: ")
                self.cursor.execute(f'select RoleName, RoleDescription from WorkerRole where '
                                    f'RoleID = {answer[3]}')
                answer = answer[:3] + self.cursor.fetchone() + answer[-1:]
        for index in range(len(answer)):
            information += '\n' + textwrap.fill(headers[index] + ("Не указано" if answer[index] is None
                                                                  else str(answer[index])), 50)
        information = information[1:]
        return information

    @sql
    def update_log(self):
        self.cursor.execute(f'update {self.user_group} set LastLog = current_timestamp() where PersonID = '
                            f'{self.user_id}')
        self.cursor.connection.commit()

    @sql
    def create_course(self, name, subject, year):
        subject = "null" if subject == '' else f'"{subject}"'
        year = "null" if year == '' else year
        self.cursor.execute(f'insert Course(CourseName, CourseSubject, CourseNumber) '
                            f'values ("{name}", {subject}, {year})')
        self.cursor.connection.commit()

    @sql
    def course_is_my(self, course_id):
        self.cursor.execute(f'select exists(select * from Course{self.user_group} where CourseID = {course_id} '
                            f'and PersonID = {self.user_id})')
        return self.cursor.fetchone()[0]

    @sql
    def connect_to_course(self, number):
        self.cursor.execute(f'insert Course{self.user_group}(CourseID, PersonID) values({number}, {self.user_id})')
        self.cursor.connection.commit()

    @sql
    def update_course_log(self, number):
        self.cursor.execute(f'update Course{self.user_group} set LastLog = current_timestamp() where CourseID = '
                            f'{number} and PersonID = {self.user_id}')
        self.cursor.connection.commit()

    @sql
    def get_all_courses(self):
        self.cursor.execute(f'select CourseID, CourseName, CourseSubject, CourseNumber from Course order by CourseID')
        return self.cursor.fetchall()

    @sql
    def get_my_courses(self):
        self.cursor.execute(f'select Course{self.user_group}.CourseID, CourseName, CourseSubject, CourseNumber from '
                            f'Course{self.user_group} join Course on Course.CourseID = Course{self.user_group}.CourseID'
                            f' where PersonID = {self.user_id}')
        return self.cursor.fetchall()

    @sql
    def get_course_name(self, number):
        self.cursor.execute(f'select CourseName from Course where CourseID = {number}')
        return self.cursor.fetchone()[0]

    @sql
    def get_theme_name(self, number):
        self.cursor.execute(f'select ThemeName from Theme where ThemeID = {number}')
        return self.cursor.fetchone()[0]

    @sql
    def get_themes(self, number):
        self.cursor.execute(f'select ThemeID, ThemeName from Theme where CourseID = {number} order by Pos')
        return self.cursor.fetchall()

    @sql
    def add_theme(self, course_id, theme_name):
        self.cursor.execute(f'call AddTheme({course_id}, "{theme_name}")')
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0]

    @sql
    def delete_theme(self, course_id, theme_id):
        self.cursor.execute(f'call DeleteTheme({course_id}, {theme_id})')
        self.cursor.connection.commit()

    @sql
    def change_theme_name(self, theme_id, theme_name):
        self.cursor.execute(f'update Theme set ThemeName = "{theme_name}" where ThemeID = {theme_id}')
        self.cursor.connection.commit()

    @sql
    def change_theme_pos(self, course_id, theme_id, position):
        self.cursor.execute(f'call ChangeThemePos({course_id}, {theme_id}, {position})')
        self.cursor.connection.commit()

    @sql
    def get_all_users(self):
        self.cursor.execute(f'select * from UsersTable order by PersonName')
        return self.cursor.fetchall()

    @sql
    def course_users(self, course_id):
        self.cursor.execute(f'select Mail, PersonName, LastLog, GroupName from CourseUsersTable where CourseID = '
                            f'{course_id} order by PersonName')
        return self.cursor.fetchall()

    @sql
    def get_materials(self, theme_id):
        self.cursor.execute(f'select LessonID, LessonName from Lesson where ThemeID = {theme_id} order by Pos')
        output = [['Занятие', self.cursor.fetchall()]]
        self.cursor.execute(f'select QuestionID, QuestionName from Question where ThemeID = {theme_id} order by Pos')
        output.append(['Вопрос', list(self.cursor.fetchall())])
        return output

    @sql
    def get_lesson(self, lesson_id):
        self.cursor.execute(f'select LessonName, RawText, URL from Lesson where LessonID = {lesson_id}')
        return self.cursor.fetchone()

    @sql
    def get_question(self, question_id):
        self.cursor.execute(f'call GetTask({question_id}, {self.user_id})')
        return self.cursor.fetchone()

    @sql
    def add_question_result(self, task_id, answer, result):
        self.cursor.execute(f'insert Result(TaskID, PersonID, Answer, Truth) values ({task_id}, {self.user_id}'
                            f', "{answer}", {result})')
        self.cursor.connection.commit()

    @sql
    def get_my_results(self, theme_id):
        self.cursor.execute(f'call GetMyResults({theme_id}, {self.user_id})')
        return self.cursor.fetchall()

    class DBException(Exception):
        def __init__(self, message):
            super().__init__(message)

    def close(self):
        if self.user_id is not None:
            self.update_log()
        self.cursor.connection.close()
