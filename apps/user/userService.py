#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "David"
# Date  : 2021-11-22
# Digest:


from apps.base.service import BaseSqlService
from apps.user.studentService import StudentService
from apps.user.teacherService import TeacherService
from apps.classes.classService import ClassService
from tools.error import BaseError
from tools.usual import auth_password


class UserService(BaseSqlService):
    """
    用户service
    """

    @staticmethod
    def auth_user_login(identify, username, password):
        """
        用户登录
        :param identify: 身份
        :param username: 用户名
        :param password: 密码
        :return:
        """
        if identify == "student":
            user_obj = StudentService()
        else:
            user_obj = TeacherService()

        userinfo = user_obj.query_userinfo(username)
        if not userinfo:
            raise BaseError(msg="未查询到该用户")

        if not auth_password(password, userinfo["password"]):
            raise BaseError(msg="密码错误")

        if identify == "student":
            user_uid = userinfo["student_uid"]
        else:
            user_uid = userinfo["teacher_uid"]

        return user_uid

    @staticmethod
    def query_user_profile(identify, user_uid):
        """
        查询个人信息
        :param identify: 身份
        :param user_uid: 用户ID
        :return:
        """
        if identify == "student":
            user_obj = StudentService()
        else:
            user_obj = TeacherService()

        profile = user_obj.query_profile(user_uid)

        if identify == "student":
            class_name = ""
            student_name = profile["student_name"]
            # 查询班级
            class_uid = profile["class_uid"]
            if class_uid:
                class_obj = ClassService()
                classes = class_obj.query_class_by_class_uid_list([class_uid])
                if classes:
                    class_name = classes[0]["class_name"]

            name = f"{class_name} {student_name}"

        else:
            name = profile["teacher_name"]

        data = {
            "name": name
        }
        return data
